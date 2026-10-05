"""Apify Actor Entrypoint: Global Football Intelligence & Poisson H2H Predictor."""

import asyncio
import os
from apify import Actor
from src.leagues_database import LEAGUES_DATABASE, LeaguesManager
from src.matches_engine import LEAGUES_MATCHES
from src.players_stats import PLAYERS_LEADERBOARD
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

        Actor.log.info(f"Processing Football Intelligence across {len(target_leagues)} competitions...")
        if api_key:
            Actor.log.info("API Key / Token authentication provided.")

        dataset_records = []

        # 1. League Records (Standings, Matches, Players)
        for league_name in target_leagues:
            league_meta = LEAGUES_DATABASE[league_name]
            record = {
                "record_type": "competition_summary",
                "competition_name": league_name,
                "competition_id": league_meta.get("id"),
                "country": league_meta.get("country"),
                "confederation": league_meta.get("confederation"),
                "type": league_meta.get("type"),
                "market_value": league_meta.get("market_value"),
                "teams_count": league_meta.get("teams_count"),
                "avg_goals_per_game": league_meta.get("avg_goals_per_game"),
                "defending_champion": league_meta.get("defending_champion"),
                "most_successful_club": league_meta.get("most_successful")
            }

            if include_standings:
                record["standings"] = league_meta.get("standings", [])

            if include_matches and league_name in LEAGUES_MATCHES:
                record["matches_and_fixtures"] = LEAGUES_MATCHES[league_name]

            if include_players and league_name in PLAYERS_LEADERBOARD:
                record["players_leaderboard"] = PLAYERS_LEADERBOARD[league_name]

            dataset_records.append(record)

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
            Actor.log.info(f"Successfully pushed {len(dataset_records)} football intelligence records to Apify dataset.")

        # Save executive summary in Key-Value store for Apify MCP & instant API tools
        summary_payload = {
            "totalCompetitionsAnalyzed": len(target_leagues),
            "competitions": target_leagues,
            "h2hSimulation": {
                "matchup": f"{h2h_home} vs {h2h_away}",
                "homeWinPct": h2h_result.get("p_home"),
                "drawPct": h2h_result.get("p_draw"),
                "awayWinPct": h2h_result.get("p_away"),
                "topScoreline": h2h_result.get("top_scorelines", [("N/A", 0)])[0][0] if h2h_result.get("top_scorelines") else "N/A"
            },
            "leaguesOverview": [
                {
                    "name": rec["competition_name"],
                    "country": rec["country"],
                    "teams": rec["teams_count"],
                    "leader": rec.get("standings", [{}])[0].get("team", "N/A") if rec.get("standings") else "N/A"
                }
                for rec in dataset_records if rec.get("record_type") == "competition_summary"
            ]
        }
        await Actor.set_value("OUTPUT", summary_payload)
        Actor.log.info("Stored football summary OUTPUT in Key-Value store.")

if __name__ == "__main__":
    asyncio.run(main())
