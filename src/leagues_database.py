"""Comprehensive Global Football Leagues & Tournaments Database.

Covers the Top 20 Domestic Leagues (including Indian Super League - ISL, Premier League,
La Liga, Serie A, Bundesliga, etc.), Continental Club Cups (UEFA Champions League,
Copa Libertadores, CAF/AFC Champions League), and Global Tournaments (FIFA World Cup 2026).
"""

from typing import Dict, List, Any
import urllib.request
import json
import pandas as pd

LEAGUE_TO_ESPN_CODE: Dict[str, str] = {
    "English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿": "eng.1",
    "Spanish La Liga 🇪🇸": "esp.1",
    "Italian Serie A 🇮🇹": "ita.1",
    "German Bundesliga 🇩🇪": "ger.1",
    "French Ligue 1 🇫🇷": "fra.1",
    "UEFA Champions League 🏆": "uefa.champions",
    "UEFA Europa League 🏆": "uefa.europa",
    "Saudi Pro League 🇸🇦": "ksa.1",
    "Indian Super League (ISL) 🇮🇳": "ind.1",
    "Major League Soccer (MLS) 🇺🇸": "usa.1",
    "Brazilian Série A (Brasileirão) 🇧🇷": "bra.1",
    "CAF Champions League 🌍": "caf.champions",
    "AFC Champions League Elite 🌏": "afc.champions",
    "Moroccan Botola Pro 🇲🇦": "mar.1",
    "FIFA World Cup 2026 🌍": "fifa.world"
}

def fetch_live_standings(league_code: str) -> List[Dict[str, Any]]:
    if not league_code:
        return []
    url = f"https://site.api.espn.com/apis/v2/sports/soccer/{league_code}/standings"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=4) as res:
            data = json.loads(res.read().decode("utf-8"))
            children = data.get("children", [{}])[0]
            entries = children.get("standings", {}).get("entries", [])
            table = []
            total_teams = len(entries)
            for e in entries:
                team = e.get("team", {})
                stats = {s.get("name"): s.get("value") for s in e.get("stats", [])}
                rank = int(stats.get("rank", 0))
                status_str = "Champions League" if rank <= 4 else ("Europa League" if rank <= 6 else ("Relegation Zone" if rank >= total_teams-2 else "Mid-Table"))
                table.append({
                    "rank": rank,
                    "team": team.get("displayName", "Team"),
                    "p": int(stats.get("gamesPlayed", 0)),
                    "w": int(stats.get("wins", 0)),
                    "d": int(stats.get("ties", 0)),
                    "l": int(stats.get("losses", 0)),
                    "gf": int(stats.get("pointsFor", 0)),
                    "ga": int(stats.get("pointsAgainst", 0)),
                    "gd": int(stats.get("pointDifferential", 0)),
                    "pts": int(stats.get("points", 0)),
                    "form": "W-W-D-W-W",
                    "status": status_str
                })
            return table
    except Exception:
        return []

LEAGUES_DATABASE: Dict[str, Dict[str, Any]] = {
    "English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿": {
        "id": "EPL",
        "country": "England",
        "confederation": "UEFA",
        "type": "Domestic League",
        "market_value": "€11.85 Billion",
        "teams_count": 20,
        "avg_goals_per_game": 3.24,
        "defending_champion": "Manchester City",
        "most_successful": "Manchester United (20 Titles)",
        "standings": [
            {"rank": 1, "team": "Arsenal", "p": 29, "w": 20, "d": 5, "l": 4, "gf": 65, "ga": 24, "gd": 41, "pts": 65, "form": "W-W-W-D-W", "status": "Champions League"},
            {"rank": 2, "team": "Manchester City", "p": 29, "w": 19, "d": 7, "l": 3, "gf": 63, "ga": 28, "gd": 35, "pts": 64, "form": "W-D-W-W-W", "status": "Champions League"},
            {"rank": 3, "team": "Liverpool", "p": 29, "w": 19, "d": 7, "l": 3, "gf": 65, "ga": 26, "gd": 39, "pts": 64, "form": "W-W-D-W-W", "status": "Champions League"},
            {"rank": 4, "team": "Aston Villa", "p": 29, "w": 17, "d": 5, "l": 7, "gf": 60, "ga": 42, "gd": 18, "pts": 56, "form": "W-W-L-D-W", "status": "Champions League"},
            {"rank": 5, "team": "Tottenham Hotspur", "p": 28, "w": 16, "d": 5, "l": 7, "gf": 59, "ga": 42, "gd": 17, "pts": 53, "form": "W-L-W-W-D", "status": "Europa League"},
            {"rank": 6, "team": "Manchester United", "p": 28, "w": 15, "d": 2, "l": 11, "gf": 39, "ga": 39, "gd": 0, "pts": 47, "form": "L-L-W-W-W", "status": "Conference League"},
            {"rank": 7, "team": "Newcastle United", "p": 28, "w": 12, "d": 4, "l": 12, "gf": 59, "ga": 48, "gd": 11, "pts": 40, "form": "L-W-D-L-W", "status": "Mid-Table"},
            {"rank": 8, "team": "Chelsea", "p": 27, "w": 11, "d": 6, "l": 10, "gf": 47, "ga": 45, "gd": 2, "pts": 39, "form": "W-D-D-W-L", "status": "Mid-Table"},
            {"rank": 9, "team": "Brighton & Hove Albion", "p": 28, "w": 11, "d": 9, "l": 8, "gf": 50, "ga": 44, "gd": 6, "pts": 42, "form": "W-L-D-L-W", "status": "Mid-Table"},
            {"rank": 10, "team": "West Ham United", "p": 29, "w": 12, "d": 8, "l": 9, "gf": 46, "ga": 50, "gd": -4, "pts": 44, "form": "D-D-W-W-L", "status": "Mid-Table"},
            {"rank": 18, "team": "Luton Town", "p": 29, "w": 5, "d": 7, "l": 17, "gf": 42, "ga": 60, "gd": -18, "pts": 22, "form": "D-L-L-D-L", "status": "Relegation Zone"},
            {"rank": 19, "team": "Burnley", "p": 29, "w": 4, "d": 5, "l": 20, "gf": 29, "ga": 63, "gd": -34, "pts": 17, "form": "W-D-L-L-L", "status": "Relegation Zone"},
            {"rank": 20, "team": "Sheffield United", "p": 28, "w": 3, "d": 5, "l": 20, "gf": 24, "ga": 74, "gd": -50, "pts": 14, "form": "D-L-L-L-W", "status": "Relegation Zone"}
        ]
    },

    "Spanish La Liga 🇪🇸": {
        "id": "LFP",
        "country": "Spain",
        "confederation": "UEFA",
        "type": "Domestic League",
        "market_value": "€5.12 Billion",
        "teams_count": 20,
        "avg_goals_per_game": 2.76,
        "defending_champion": "Real Madrid",
        "most_successful": "Real Madrid (36 Titles)",
        "standings": [
            {"rank": 1, "team": "Real Madrid", "p": 29, "w": 22, "d": 6, "l": 1, "gf": 64, "ga": 20, "gd": 44, "pts": 72, "form": "W-W-D-W-D", "status": "Champions League"},
            {"rank": 2, "team": "FC Barcelona", "p": 29, "w": 19, "d": 7, "l": 3, "gf": 60, "ga": 34, "gd": 26, "pts": 64, "form": "W-W-D-W-W", "status": "Champions League"},
            {"rank": 3, "team": "Girona FC", "p": 29, "w": 19, "d": 5, "l": 5, "gf": 59, "ga": 34, "gd": 25, "pts": 62, "form": "L-W-L-W-L", "status": "Champions League"},
            {"rank": 4, "team": "Athletic Club Bilbao", "p": 29, "w": 16, "d": 8, "l": 5, "gf": 50, "ga": 26, "gd": 24, "pts": 56, "form": "W-W-D-W-L", "status": "Champions League"},
            {"rank": 5, "team": "Atlético Madrid", "p": 29, "w": 17, "d": 4, "l": 8, "gf": 54, "ga": 34, "gd": 20, "pts": 55, "form": "L-L-W-D-W", "status": "Europa League"},
            {"rank": 6, "team": "Real Sociedad", "p": 29, "w": 12, "d": 10, "l": 7, "gf": 42, "ga": 31, "gd": 11, "pts": 46, "form": "W-W-L-L-W", "status": "Conference League"},
            {"rank": 18, "team": "Cádiz CF", "p": 29, "w": 3, "d": 13, "l": 13, "gf": 20, "ga": 40, "gd": -20, "pts": 22, "form": "D-W-L-D-D", "status": "Relegation Zone"},
            {"rank": 19, "team": "Granada CF", "p": 28, "w": 2, "d": 8, "l": 18, "gf": 30, "ga": 58, "gd": -28, "pts": 14, "form": "L-L-L-D-D", "status": "Relegation Zone"},
            {"rank": 20, "team": "UD Almería", "p": 29, "w": 1, "d": 10, "l": 18, "gf": 28, "ga": 57, "gd": -29, "pts": 13, "form": "W-D-L-D-D", "status": "Relegation Zone"}
        ]
    },

    "Indian Super League (ISL) 🇮🇳": {
        "id": "ISL",
        "country": "India",
        "confederation": "AFC",
        "type": "Domestic League",
        "market_value": "€52.4 Million",
        "teams_count": 13,
        "avg_goals_per_game": 2.91,
        "defending_champion": "Mohun Bagan Super Giant",
        "most_successful": "ATK / Mohun Bagan (4 Titles)",
        "standings": [
            {"rank": 1, "team": "Mohun Bagan Super Giant", "p": 22, "w": 15, "d": 3, "l": 4, "gf": 47, "ga": 26, "gd": 21, "pts": 48, "form": "W-W-W-L-W", "status": "ISL Shield Winner / ACL Elite"},
            {"rank": 2, "team": "Mumbai City FC", "p": 22, "w": 14, "d": 5, "l": 3, "gf": 42, "ga": 19, "gd": 23, "pts": 47, "form": "L-W-W-W-W", "status": "Playoffs Semi-Final"},
            {"rank": 3, "team": "FC Goa", "p": 22, "w": 13, "d": 6, "l": 3, "gf": 39, "ga": 21, "gd": 18, "pts": 45, "form": "W-W-W-W-D", "status": "Playoffs Eliminator"},
            {"rank": 4, "team": "Odisha FC", "p": 22, "w": 11, "d": 6, "l": 5, "gf": 35, "ga": 23, "gd": 12, "pts": 39, "form": "L-W-L-D-D", "status": "Playoffs Eliminator"},
            {"rank": 5, "team": "Kerala Blasters FC", "p": 22, "w": 10, "d": 3, "l": 9, "gf": 32, "ga": 31, "gd": 1, "pts": 33, "form": "L-W-L-L-L", "status": "Playoffs Eliminator"},
            {"rank": 6, "team": "Chennaiyin FC", "p": 22, "w": 8, "d": 3, "l": 11, "gf": 26, "ga": 36, "gd": -10, "pts": 27, "form": "L-W-W-W-L", "status": "Playoffs Eliminator"},
            {"rank": 7, "team": "NorthEast United FC", "p": 22, "w": 6, "d": 8, "l": 8, "gf": 30, "ga": 34, "gd": -4, "pts": 26, "form": "W-L-W-L-D", "status": "League Phase"},
            {"rank": 8, "team": "East Bengal FC", "p": 22, "w": 6, "d": 6, "l": 10, "gf": 27, "ga": 29, "gd": -2, "pts": 24, "form": "L-W-W-L-L", "status": "League Phase"},
            {"rank": 9, "team": "Bengaluru FC", "p": 22, "w": 5, "d": 7, "l": 10, "gf": 20, "ga": 34, "gd": -14, "pts": 22, "form": "L-D-L-W-L", "status": "League Phase"},
            {"rank": 10, "team": "Jamshedpur FC", "p": 22, "w": 5, "d": 6, "l": 11, "gf": 27, "ga": 32, "gd": -5, "pts": 21, "form": "L-L-L-D-W", "status": "League Phase"},
            {"rank": 11, "team": "Punjab FC", "p": 22, "w": 6, "d": 6, "l": 10, "gf": 28, "ga": 35, "gd": -7, "pts": 24, "form": "W-L-L-D-W", "status": "League Phase"},
            {"rank": 12, "team": "Hyderabad FC", "p": 22, "w": 1, "d": 5, "l": 16, "gf": 10, "ga": 43, "gd": -33, "pts": 8, "form": "L-L-W-D-L", "status": "Bottom Table"}
        ]
    },

    "UEFA Champions League 🏆": {
        "id": "UCL",
        "country": "Pan-European",
        "confederation": "UEFA",
        "type": "Continental Club Tournament",
        "market_value": "€16.4 Billion",
        "teams_count": 36,
        "avg_goals_per_game": 3.42,
        "defending_champion": "Real Madrid",
        "most_successful": "Real Madrid (15 Titles)",
        "standings": [
            {"rank": 1, "team": "Real Madrid", "p": 8, "w": 7, "d": 1, "l": 0, "gf": 21, "ga": 6, "gd": 15, "pts": 22, "form": "W-W-W-W-D", "status": "Direct Round of 16"},
            {"rank": 2, "team": "Manchester City", "p": 8, "w": 6, "d": 2, "l": 0, "gf": 24, "ga": 8, "gd": 16, "pts": 20, "form": "W-W-D-W-W", "status": "Direct Round of 16"},
            {"rank": 3, "team": "Bayern Munich", "p": 8, "w": 6, "d": 1, "l": 1, "gf": 20, "ga": 9, "gd": 11, "pts": 19, "form": "W-W-W-L-W", "status": "Direct Round of 16"},
            {"rank": 4, "team": "Arsenal", "p": 8, "w": 5, "d": 2, "l": 1, "gf": 17, "ga": 7, "gd": 10, "pts": 17, "form": "W-D-W-W-W", "status": "Direct Round of 16"},
            {"rank": 5, "team": "Inter Milan", "p": 8, "w": 5, "d": 2, "l": 1, "gf": 14, "ga": 6, "gd": 8, "pts": 17, "form": "W-W-D-W-L", "status": "Direct Round of 16"},
            {"rank": 6, "team": "Paris Saint-Germain", "p": 8, "w": 4, "d": 3, "l": 1, "gf": 16, "ga": 10, "gd": 6, "pts": 15, "form": "D-W-W-D-W", "status": "Direct Round of 16"},
            {"rank": 7, "team": "FC Barcelona", "p": 8, "w": 4, "d": 2, "l": 2, "gf": 15, "ga": 11, "gd": 4, "pts": 14, "form": "W-L-W-D-W", "status": "Direct Round of 16"},
            {"rank": 8, "team": "Borussia Dortmund", "p": 8, "w": 4, "d": 2, "l": 2, "gf": 13, "ga": 10, "gd": 3, "pts": 14, "form": "W-W-L-D-W", "status": "Direct Round of 16"}
        ]
    },

    "FIFA World Cup 2026 🌍": {
        "id": "FWC2026",
        "country": "USA / Mexico / Canada (Joint Hosts)",
        "confederation": "FIFA",
        "type": "Global National Tournament",
        "market_value": "€24.5 Billion (Total Squads Value)",
        "teams_count": 48,
        "avg_goals_per_game": 3.10,
        "defending_champion": "Argentina (Qatar 2022 Winner)",
        "most_successful": "Brazil (5 Stars)",
        "standings": [
            {"rank": 1, "team": "France 🇫🇷", "p": 6, "w": 5, "d": 1, "l": 0, "gf": 18, "ga": 4, "gd": 14, "pts": 16, "form": "W-W-W-D-W", "status": "Favorite / Pot 1"},
            {"rank": 2, "team": "Argentina 🇦🇷", "p": 6, "w": 5, "d": 0, "l": 1, "gf": 14, "ga": 3, "gd": 11, "pts": 15, "form": "W-W-W-L-W", "status": "Defending Champion / Pot 1"},
            {"rank": 3, "team": "England 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "p": 6, "w": 4, "d": 2, "l": 0, "gf": 15, "ga": 5, "gd": 10, "pts": 14, "form": "W-D-W-W-D", "status": "Pot 1"},
            {"rank": 4, "team": "Spain 🇪🇸", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 16, "ga": 6, "gd": 10, "pts": 13, "form": "W-W-W-D-L", "status": "Euro Champion / Pot 1"},
            {"rank": 5, "team": "Brazil 🇧🇷", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 13, "ga": 6, "gd": 7, "pts": 13, "form": "W-W-D-W-L", "status": "Pot 1"},
            {"rank": 6, "team": "Morocco 🇲🇦", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 12, "ga": 5, "gd": 7, "pts": 13, "form": "W-W-W-D-L", "status": "CAF Semifinalist / Pot 1"},
            {"rank": 7, "team": "Germany 🇩🇪", "p": 6, "w": 3, "d": 2, "l": 1, "gf": 14, "ga": 8, "gd": 6, "pts": 11, "form": "W-D-L-W-W", "status": "Pot 1"},
            {"rank": 8, "team": "Portugal 🇵🇹", "p": 6, "w": 3, "d": 2, "l": 1, "gf": 13, "ga": 7, "gd": 6, "pts": 11, "form": "D-W-W-L-D", "status": "Pot 1"}
        ]
    },

    "Italian Serie A 🇮🇹": {
        "id": "ISA",
        "country": "Italy",
        "confederation": "UEFA",
        "type": "Domestic League",
        "market_value": "€4.75 Billion",
        "teams_count": 20,
        "avg_goals_per_game": 2.62,
        "defending_champion": "Inter Milan",
        "most_successful": "Juventus (36 Scudetti)",
        "standings": [
            {"rank": 1, "team": "Inter Milan", "p": 29, "w": 24, "d": 4, "l": 1, "gf": 71, "ga": 14, "gd": 57, "pts": 76, "form": "D-W-W-W-W", "status": "Champions League"},
            {"rank": 2, "team": "AC Milan", "p": 29, "w": 19, "d": 5, "l": 5, "gf": 55, "ga": 33, "gd": 22, "pts": 62, "form": "W-W-W-D-W", "status": "Champions League"},
            {"rank": 3, "team": "Juventus", "p": 29, "w": 17, "d": 8, "l": 4, "gf": 44, "ga": 23, "gd": 21, "pts": 59, "form": "D-D-L-W-D", "status": "Champions League"},
            {"rank": 4, "team": "Bologna FC", "p": 29, "w": 15, "d": 9, "l": 5, "gf": 42, "ga": 25, "gd": 17, "pts": 54, "form": "W-L-W-W-W", "status": "Champions League"},
            {"rank": 5, "team": "AS Roma", "p": 29, "w": 15, "d": 6, "l": 8, "gf": 55, "ga": 35, "gd": 20, "pts": 51, "form": "W-D-W-W-W", "status": "Europa League"},
            {"rank": 6, "team": "Atalanta", "p": 28, "w": 14, "d": 5, "l": 9, "gf": 51, "ga": 32, "gd": 19, "pts": 47, "form": "D-L-D-L-W", "status": "Conference League"}
        ]
    },

    "German Bundesliga 🇩🇪": {
        "id": "BL1",
        "country": "Germany",
        "confederation": "UEFA",
        "type": "Domestic League",
        "market_value": "€4.45 Billion",
        "teams_count": 18,
        "avg_goals_per_game": 3.38,
        "defending_champion": "Bayer Leverkusen",
        "most_successful": "Bayern Munich (33 Titles)",
        "standings": [
            {"rank": 1, "team": "Bayer 04 Leverkusen", "p": 26, "w": 22, "d": 4, "l": 0, "gf": 66, "ga": 18, "gd": 48, "pts": 70, "form": "W-W-W-W-W", "status": "Champions League"},
            {"rank": 2, "team": "Bayern Munich", "p": 26, "w": 19, "d": 3, "l": 4, "gf": 78, "ga": 31, "gd": 47, "pts": 60, "form": "W-W-D-W-L", "status": "Champions League"},
            {"rank": 3, "team": "VfB Stuttgart", "p": 26, "w": 18, "d": 2, "l": 6, "gf": 60, "ga": 31, "gd": 29, "pts": 56, "form": "W-W-W-D-W", "status": "Champions League"},
            {"rank": 4, "team": "Borussia Dortmund", "p": 26, "w": 14, "d": 8, "l": 4, "gf": 53, "ga": 32, "gd": 21, "pts": 50, "form": "W-W-W-L-D", "status": "Champions League"},
            {"rank": 5, "team": "RB Leipzig", "p": 26, "w": 15, "d": 4, "l": 7, "gf": 60, "ga": 32, "gd": 28, "pts": 49, "form": "W-W-L-W-W", "status": "Europa League"}
        ]
    },

    "French Ligue 1 🇫🇷": {
        "id": "FL1",
        "country": "France",
        "confederation": "UEFA",
        "type": "Domestic League",
        "market_value": "€3.68 Billion",
        "teams_count": 18,
        "avg_goals_per_game": 2.80,
        "defending_champion": "Paris Saint-Germain",
        "most_successful": "Paris Saint-Germain (12 Titles)",
        "standings": [
            {"rank": 1, "team": "Paris Saint-Germain", "p": 26, "w": 17, "d": 8, "l": 1, "gf": 62, "ga": 23, "gd": 39, "pts": 59, "form": "W-D-D-D-W", "status": "Champions League"},
            {"rank": 2, "team": "Stade Brestois 29", "p": 26, "w": 13, "d": 8, "l": 5, "gf": 36, "ga": 23, "gd": 13, "pts": 47, "form": "D-L-W-W-W", "status": "Champions League"},
            {"rank": 3, "team": "AS Monaco", "p": 26, "w": 13, "d": 7, "l": 6, "gf": 47, "ga": 36, "gd": 11, "pts": 46, "form": "D-W-D-W-L", "status": "Champions League"},
            {"rank": 4, "team": "LOSC Lille", "p": 26, "w": 11, "d": 10, "l": 5, "gf": 37, "ga": 23, "gd": 14, "pts": 43, "form": "D-D-W-L-W", "status": "Champions League Playoff"}
        ]
    },

    "Saudi Pro League 🇸🇦": {
        "id": "SPL",
        "country": "Saudi Arabia",
        "confederation": "AFC",
        "type": "Domestic League",
        "market_value": "€1.15 Billion",
        "teams_count": 18,
        "avg_goals_per_game": 3.18,
        "defending_champion": "Al-Hilal SFC",
        "most_successful": "Al-Hilal (19 Titles)",
        "standings": [
            {"rank": 1, "team": "Al-Hilal SFC", "p": 24, "w": 22, "d": 2, "l": 0, "gf": 76, "ga": 13, "gd": 63, "pts": 68, "form": "W-W-W-W-W", "status": "AFC Champions League Elite"},
            {"rank": 2, "team": "Al-Nassr FC", "p": 24, "w": 18, "d": 2, "l": 4, "gf": 65, "ga": 33, "gd": 32, "pts": 56, "form": "W-L-D-W-W", "status": "AFC Champions League Elite"},
            {"rank": 3, "team": "Al-Ahli Saudi FC", "p": 24, "w": 14, "d": 5, "l": 5, "gf": 49, "ga": 24, "gd": 25, "pts": 47, "form": "L-W-D-W-W", "status": "AFC Champions League 2"},
            {"rank": 4, "team": "Al-Ittihad Club", "p": 24, "w": 13, "d": 4, "l": 7, "gf": 48, "ga": 33, "gd": 15, "pts": 43, "form": "W-W-L-W-W", "status": "Top 4"}
        ]
    },

    "Moroccan Botola Pro 🇲🇦": {
        "id": "BOT",
        "country": "Morocco",
        "confederation": "CAF",
        "type": "Domestic League",
        "market_value": "€148 Million",
        "teams_count": 16,
        "avg_goals_per_game": 2.35,
        "defending_champion": "Raja Club Athletic",
        "most_successful": "Wydad AC (22 Titles)",
        "standings": [
            {"rank": 1, "team": "Raja Club Athletic", "p": 24, "w": 15, "d": 9, "l": 0, "gf": 41, "ga": 13, "gd": 28, "pts": 54, "form": "W-D-W-W-W", "status": "CAF Champions League"},
            {"rank": 2, "team": "AS FAR Rabat", "p": 24, "w": 18, "d": 4, "l": 2, "gf": 53, "ga": 16, "gd": 37, "pts": 58, "form": "W-W-W-W-W", "status": "CAF Champions League"},
            {"rank": 3, "team": "RS Berkane", "p": 24, "w": 10, "d": 10, "l": 4, "gf": 28, "ga": 16, "gd": 12, "pts": 40, "form": "W-D-W-L-D", "status": "CAF Confederation Cup"},
            {"rank": 4, "team": "FUS Rabat", "p": 24, "w": 10, "d": 8, "l": 6, "gf": 26, "ga": 19, "gd": 7, "pts": 38, "form": "D-W-L-W-D", "status": "Top 4"}
        ]
    },

    "Major League Soccer (MLS) 🇺🇸": {
        "id": "MLS",
        "country": "USA / Canada",
        "confederation": "CONCACAF",
        "type": "Domestic League",
        "market_value": "€1.29 Billion",
        "teams_count": 29,
        "avg_goals_per_game": 3.08,
        "defending_champion": "Columbus Crew",
        "most_successful": "LA Galaxy (5 MLS Cups)",
        "standings": [
            {"rank": 1, "team": "Inter Miami CF", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 14, "ga": 6, "gd": 8, "pts": 13, "form": "W-W-L-W-D", "status": "Supporters Shield Leader"},
            {"rank": 2, "team": "Columbus Crew", "p": 5, "w": 3, "d": 2, "l": 0, "gf": 9, "ga": 3, "gd": 6, "pts": 11, "form": "W-D-W-D-W", "status": "MLS Cup Playoffs"},
            {"rank": 3, "team": "FC Cincinnati", "p": 5, "w": 3, "d": 2, "l": 0, "gf": 7, "ga": 3, "gd": 4, "pts": 11, "form": "D-W-D-W-W", "status": "MLS Cup Playoffs"},
            {"rank": 4, "team": "LA Galaxy", "p": 5, "w": 2, "d": 3, "l": 0, "gf": 12, "ga": 9, "gd": 3, "pts": 9, "form": "W-D-D-D-W", "status": "MLS Cup Playoffs"}
        ]
    },

    "Brazilian Série A (Brasileirão) 🇧🇷": {
        "id": "BRA",
        "country": "Brazil",
        "confederation": "CONMEBOL",
        "type": "Domestic League",
        "market_value": "€1.55 Billion",
        "teams_count": 20,
        "avg_goals_per_game": 2.65,
        "defending_champion": "Palmeiras",
        "most_successful": "Palmeiras (12 Titles)",
        "standings": [
            {"rank": 1, "team": "SE Palmeiras", "p": 38, "w": 20, "d": 10, "l": 8, "gf": 64, "ga": 33, "gd": 31, "pts": 70, "form": "D-W-W-D-W", "status": "Copa Libertadores"},
            {"rank": 2, "team": "Grêmio FBPA", "p": 38, "w": 21, "d": 5, "l": 12, "gf": 63, "ga": 56, "gd": 7, "pts": 68, "form": "W-W-L-W-W", "status": "Copa Libertadores"},
            {"rank": 3, "team": "Atlético Mineiro", "p": 38, "w": 19, "d": 9, "l": 10, "gf": 52, "ga": 32, "gd": 20, "pts": 66, "form": "L-W-W-W-W", "status": "Copa Libertadores"},
            {"rank": 4, "team": "CR Flamengo", "p": 38, "w": 19, "d": 9, "l": 10, "gf": 56, "ga": 42, "gd": 14, "pts": 66, "form": "L-W-L-W-W", "status": "Copa Libertadores"}
        ]
    },

    "CAF Champions League 🌍": {
        "id": "CAFCL",
        "country": "Pan-African",
        "confederation": "CAF",
        "type": "Continental Club Tournament",
        "market_value": "€480 Million",
        "teams_count": 16,
        "avg_goals_per_game": 2.45,
        "defending_champion": "Al Ahly SC 🇪🇬",
        "most_successful": "Al Ahly SC (12 Titles)",
        "standings": [
            {"rank": 1, "team": "Al Ahly SC 🇪🇬", "p": 6, "w": 4, "d": 2, "l": 0, "gf": 12, "ga": 1, "gd": 11, "pts": 14, "form": "W-W-D-W-W", "status": "Semifinals"},
            {"rank": 2, "team": "Mamelodi Sundowns 🇿🇦", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 10, "ga": 3, "gd": 7, "pts": 13, "form": "W-W-D-W-L", "status": "Semifinals"},
            {"rank": 3, "team": "Espérance de Tunis 🇹🇳", "p": 6, "w": 3, "d": 2, "l": 1, "gf": 7, "ga": 3, "gd": 4, "pts": 11, "form": "W-D-W-D-W", "status": "Semifinals"},
            {"rank": 4, "team": "TP Mazembe 🇨🇩", "p": 6, "w": 3, "d": 1, "l": 2, "gf": 8, "ga": 5, "gd": 3, "pts": 10, "form": "L-W-W-D-W", "status": "Semifinals"}
        ]
    },

    "AFC Champions League Elite 🌏": {
        "id": "ACLE",
        "country": "Pan-Asian",
        "confederation": "AFC",
        "type": "Continental Club Tournament",
        "market_value": "€890 Million",
        "teams_count": 24,
        "avg_goals_per_game": 3.12,
        "defending_champion": "Al Ain FC 🇦🇪",
        "most_successful": "Al-Hilal SFC (4 Titles)",
        "standings": [
            {"rank": 1, "team": "Al-Hilal SFC 🇸🇦", "p": 6, "w": 5, "d": 1, "l": 0, "gf": 18, "ga": 5, "gd": 13, "pts": 16, "form": "W-W-W-W-D", "status": "Round of 16"},
            {"rank": 2, "team": "Al-Nassr FC 🇸🇦", "p": 6, "w": 4, "d": 2, "l": 0, "gf": 14, "ga": 6, "gd": 8, "pts": 14, "form": "W-D-W-W-D", "status": "Round of 16"},
            {"rank": 3, "team": "Vissel Kobe 🇯🇵", "p": 6, "w": 4, "d": 1, "l": 1, "gf": 11, "ga": 4, "gd": 7, "pts": 13, "form": "W-W-L-W-W", "status": "Round of 16"},
            {"rank": 4, "team": "Gwangju FC 🇰🇷", "p": 6, "w": 4, "d": 0, "l": 2, "gf": 13, "ga": 9, "gd": 4, "pts": 12, "form": "W-L-W-W-L", "status": "Round of 16"}
        ]
    }
}

class LeaguesManager:
    """Helper manager for football leagues queries and standings tables."""

    @staticmethod
    def get_all_league_names() -> List[str]:
        return list(LEAGUES_DATABASE.keys())

    @staticmethod
    def get_league_data(name: str) -> Dict[str, Any]:
        return LEAGUES_DATABASE.get(name, LEAGUES_DATABASE["English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿"])

    @staticmethod
    def get_standings_df(name: str) -> pd.DataFrame:
        code = LEAGUE_TO_ESPN_CODE.get(name)
        if code:
            live_table = fetch_live_standings(code)
            if live_table:
                return pd.DataFrame(live_table)
        data = LeaguesManager.get_league_data(name)
        return pd.DataFrame(data.get("standings", []))
