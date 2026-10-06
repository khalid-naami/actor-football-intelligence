"""Apify Actor Entrypoint: Global Football Intelligence & Live Matchday Scoreboard."""

import asyncio
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apify import Actor
from src.leagues_database import LEAGUES_DATABASE, LeaguesManager
from src.matches_engine import MatchesEngine
from src.players_stats import PlayersStatsManager, PLAYERS_LEADERBOARD
from src.h2h_predictor_engine import H2HPredictorEngine

async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        selected_leagues = actor_input.get("selectedLeagues")
        include_standings = bool(actor_input.get("includeStandings", True))
        include_matches = bool(actor_input.get("includeFixturesAndLiveScores", True))
        include_players = bool(actor_input.get("includeTopScorers", True))
        simulate_h2h = bool(actor_input.get("simulateH2H", True))
        h2h_home = actor_input.get("simulateH2HHomeTeam", "Manchester City")
        h2h_away = actor_input.get("simulateH2HAwayTeam", "Arsenal")
        api_key = actor_input.get("apiKey") or os.getenv("APIFY_TOKEN") or os.getenv("API_KEY", "")

        all_leagues = LeaguesManager.get_all_league_names()
        target_leagues = [lg for lg in selected_leagues if lg in LEAGUES_DATABASE] if selected_leagues else all_leagues

        Actor.log.info(f"Processing Live Football Intelligence across {len(target_leagues)} competitions...")
        if api_key:
            Actor.log.info("API Key / Token authentication provided.")

        dataset_records = []
        live_matches_count = 0

        # 1. League Records with REAL LIVE STANDINGS & REAL LIVE MATCHES
        for league_name in target_leagues:
            league_meta = LEAGUES_DATABASE[league_name]

            # Fetch fresh real-time live standings
            standings_records = []
            if include_standings:
                try:
                    df_standings = LeaguesManager.get_standings_df(league_name)
                    standings_records = df_standings.to_dict(orient="records") if not df_standings.empty else league_meta.get("standings", [])
                except Exception as e:
                    Actor.log.warning(f"Standings fetch warning for {league_name}: {e}")
                    standings_records = league_meta.get("standings", [])

            # Fetch fresh real-time live matches & upcoming fixtures
            matches_records = []
            if include_matches:
                try:
                    matches_records = MatchesEngine.get_league_matches(league_name)
                    for m in matches_records:
                        if m.get("status") == "LIVE":
                            live_matches_count += 1
                except Exception as e:
                    Actor.log.warning(f"Matches fetch warning for {league_name}: {e}")
                    matches_records = []

            # Fetch current top scorers & assists
            players_data = {}
            if include_players:
                try:
                    df_scorers = PlayersStatsManager.get_top_scorers_df(league_name)
                    df_assists = PlayersStatsManager.get_top_assists_df(league_name)
                    players_data = {
                        "top_scorers": df_scorers.to_dict(orient="records") if not df_scorers.empty else [],
                        "top_assists": df_assists.to_dict(orient="records") if not df_assists.empty else []
                    }
                except Exception as e:
                    players_data = PLAYERS_LEADERBOARD.get(league_name, {})

            record = {
                "record_type": "competition_summary",
                "competition_name": league_name,
                "competition_id": league_meta.get("id"),
                "country": league_meta.get("country"),
                "confederation": league_meta.get("confederation"),
                "type": league_meta.get("type"),
                "market_value": league_meta.get("market_value"),
                "teams_count": len(standings_records) if standings_records else league_meta.get("teams_count"),
                "avg_goals_per_game": league_meta.get("avg_goals_per_game"),
                "defending_champion": league_meta.get("defending_champion"),
                "most_successful_club": league_meta.get("most_successful")
            }

            if include_standings:
                record["standings"] = standings_records

            if include_matches:
                record["matches_and_fixtures"] = matches_records

            if include_players:
                record["players_leaderboard"] = players_data

            dataset_records.append(record)

            # Also push individual live match records for immediate live monitoring!
            if include_matches and matches_records:
                for match_item in matches_records:
                    dataset_records.append({
                        "record_type": "live_match_event",
                        "competition_name": league_name,
                        "competition_id": league_meta.get("id"),
                        "home_team": match_item.get("home_team"),
                        "home_logo": match_item.get("home_logo"),
                        "away_team": match_item.get("away_team"),
                        "away_logo": match_item.get("away_logo"),
                        "score_home": match_item.get("score_home"),
                        "score_away": match_item.get("score_away"),
                        "status": match_item.get("status"),
                        "minute": match_item.get("minute"),
                        "stadium": match_item.get("stadium"),
                        "xg_home": match_item.get("xg_home"),
                        "xg_away": match_item.get("xg_away"),
                        "possession_home": match_item.get("possession_home"),
                        "possession_away": match_item.get("possession_away"),
                        "events": match_item.get("events", [])
                    })

        # 2. H2H Poisson Probability Simulation Record
        h2h_result = {}
        if simulate_h2h:
            Actor.log.info(f"Running H2H Poisson simulation for {h2h_home} vs {h2h_away}...")
            h2h_result = H2HPredictorEngine.calculate_match_odds(
                home_team=h2h_home,
                away_team=h2h_away,
                home_attack_rating=1.85,
                home_defense_rating=1.05,
                away_attack_rating=1.45,
                away_defense_rating=1.25,
                home_advantage=1.15
            )

            dataset_records.append({
                "record_type": "h2h_poisson_prediction",
                "home_team": h2h_home,
                "away_team": h2h_away,
                "home_expected_goals_xg": round(h2h_result["home_xg"], 2),
                "away_expected_goals_xg": round(h2h_result["away_xg"], 2),
                "win_probability_home_pct": h2h_result["p_home"],
                "draw_probability_pct": h2h_result["p_draw"],
                "win_probability_away_pct": h2h_result["p_away"],
                "over_2_5_goals_probability_pct": round(h2h_result["over_2_5_prob"] * 100, 1),
                "both_teams_to_score_btts_pct": round(h2h_result["btts_prob"] * 100, 1),
                "most_likely_scorelines": [
                    {"score": score, "probability_pct": round(prob * 100, 1)}
                    for score, prob in h2h_result.get("top_scorelines", [])
                ]
            })

        if dataset_records:
            await Actor.push_data(dataset_records)
            Actor.log.info(f"Successfully pushed {len(dataset_records)} live football records to Apify dataset.")

        # Save executive summary in Key-Value store for Apify MCP & instant API tools
        summary_payload = {
            "totalCompetitionsAnalyzed": len(target_leagues),
            "totalRecordsPushed": len(dataset_records),
            "liveMatchesDetected": live_matches_count,
            "competitions": target_leagues,
            "h2hSimulation": {
                "matchup": f"{h2h_home} vs {h2h_away}",
                "home_xg": round(h2h_result.get("home_xg", 0.0), 2),
                "away_xg": round(h2h_result.get("away_xg", 0.0), 2),
                "p_home": h2h_result.get("p_home", 0.0),
                "p_draw": h2h_result.get("p_draw", 0.0),
                "p_away": h2h_result.get("p_away", 0.0)
            }
        }
        await Actor.set_value("OUTPUT", summary_payload)
        Actor.log.info("Executive summary written to Key-Value Store key 'OUTPUT'.")

if __name__ == "__main__":
    asyncio.run(main())
