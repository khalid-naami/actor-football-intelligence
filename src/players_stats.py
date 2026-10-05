"""Elite Player Statistics, Golden Boot Scorers & Playmaker Intelligence Engine.

Provides top goalscorers, assists leaders, clean sheets, market valuations,
and radar metrics across leagues (including Premier League, La Liga, ISL, UCL, etc.).
"""

from typing import Dict, List, Any
import pandas as pd

PLAYERS_LEADERBOARD: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿": {
        "top_scorers": [
            {"rank": 1, "player": "Erling Haaland", "team": "Manchester City", "goals": 18, "pens": 2, "matches": 23, "xg": 17.4, "mins_per_goal": 105},
            {"rank": 2, "player": "Ollie Watkins", "team": "Aston Villa", "goals": 16, "pens": 0, "matches": 29, "xg": 14.8, "mins_per_goal": 158},
            {"rank": 3, "player": "Mohamed Salah", "team": "Liverpool", "goals": 15, "pens": 4, "matches": 22, "xg": 15.2, "mins_per_goal": 121},
            {"rank": 4, "player": "Dominic Solanke", "team": "Tottenham Hotspur", "goals": 14, "pens": 1, "matches": 28, "xg": 13.9, "mins_per_goal": 174},
            {"rank": 5, "player": "Bukayo Saka", "team": "Arsenal", "goals": 13, "pens": 3, "matches": 27, "xg": 11.8, "mins_per_goal": 182}
        ],
        "top_assists": [
            {"rank": 1, "player": "Bukayo Saka", "team": "Arsenal", "assists": 12, "key_passes": 74, "big_chances_created": 18},
            {"rank": 2, "player": "Cole Palmer", "team": "Chelsea", "assists": 11, "key_passes": 68, "big_chances_created": 16},
            {"rank": 3, "player": "Kevin De Bruyne", "team": "Manchester City", "assists": 10, "key_passes": 62, "big_chances_created": 17},
            {"rank": 4, "player": "Mohamed Salah", "team": "Liverpool", "assists": 9, "key_passes": 59, "big_chances_created": 15}
        ]
    },

    "Indian Super League (ISL) 🇮🇳": {
        "top_scorers": [
            {"rank": 1, "player": "Dimitrios Diamantakos", "team": "Kerala Blasters / East Bengal", "goals": 13, "pens": 3, "matches": 17, "xg": 11.8, "mins_per_goal": 110},
            {"rank": 2, "player": "Roy Krishna", "team": "Odisha FC", "goals": 13, "pens": 1, "matches": 22, "xg": 12.4, "mins_per_goal": 145},
            {"rank": 3, "player": "Jason Cummings", "team": "Mohun Bagan Super Giant", "goals": 12, "pens": 2, "matches": 22, "xg": 10.9, "mins_per_goal": 138},
            {"rank": 4, "player": "Noah Sadaoui", "team": "Kerala Blasters / FC Goa", "goals": 11, "pens": 2, "matches": 20, "xg": 10.1, "mins_per_goal": 152},
            {"rank": 5, "player": "Lallianzuala Chhangte", "team": "Mumbai City FC", "goals": 10, "pens": 1, "matches": 22, "xg": 8.9, "mins_per_goal": 185}
        ],
        "top_assists": [
            {"rank": 1, "player": "Madih Talal", "team": "East Bengal / Punjab FC", "assists": 10, "key_passes": 57, "big_chances_created": 14},
            {"rank": 2, "player": "Manvir Singh", "team": "Mohun Bagan Super Giant", "assists": 7, "key_passes": 42, "big_chances_created": 11},
            {"rank": 3, "player": "Lallianzuala Chhangte", "team": "Mumbai City FC", "assists": 6, "key_passes": 48, "big_chances_created": 12},
            {"rank": 4, "player": "Amey Ranawade", "team": "Odisha FC", "assists": 6, "key_passes": 38, "big_chances_created": 9}
        ]
    },

    "Spanish La Liga 🇪🇸": {
        "top_scorers": [
            {"rank": 1, "player": "Robert Lewandowski", "team": "FC Barcelona", "goals": 19, "pens": 2, "matches": 20, "xg": 18.2, "mins_per_goal": 92},
            {"rank": 2, "player": "Kylian Mbappé", "team": "Real Madrid", "goals": 16, "pens": 4, "matches": 21, "xg": 15.6, "mins_per_goal": 114},
            {"rank": 3, "player": "Raphinha", "team": "FC Barcelona", "goals": 13, "pens": 1, "matches": 21, "xg": 11.4, "mins_per_goal": 132},
            {"rank": 4, "player": "Vinícius Júnior", "team": "Real Madrid", "goals": 12, "pens": 2, "matches": 19, "xg": 11.8, "mins_per_goal": 135}
        ],
        "top_assists": [
            {"rank": 1, "player": "Lamine Yamal", "team": "FC Barcelona", "assists": 11, "key_passes": 61, "big_chances_created": 19},
            {"rank": 2, "player": "Raphinha", "team": "FC Barcelona", "assists": 9, "key_passes": 55, "big_chances_created": 16},
            {"rank": 3, "player": "Vinícius Júnior", "team": "Real Madrid", "assists": 8, "key_passes": 49, "big_chances_created": 14}
        ]
    }
}

PLAYER_RADAR_PROFILES: Dict[str, Dict[str, int]] = {
    "Kylian Mbappé (Real Madrid)": {"Pace ⚡": 97, "Shooting 🎯": 92, "Passing 🪄": 82, "Dribbling 🕺": 93, "Defending 🛡️": 36, "Physicality 💪": 78},
    "Erling Haaland (Man City)": {"Pace ⚡": 89, "Shooting 🎯": 96, "Passing 🪄": 68, "Dribbling 🕺": 80, "Defending 🛡️": 45, "Physicality 💪": 91},
    "Lamine Yamal (FC Barcelona)": {"Pace ⚡": 88, "Shooting 🎯": 82, "Passing 🪄": 89, "Dribbling 🕺": 94, "Defending 🛡️": 42, "Physicality 💪": 62},
    "Vinícius Júnior (Real Madrid)": {"Pace ⚡": 96, "Shooting 🎯": 86, "Passing 🪄": 83, "Dribbling 🕺": 95, "Defending 🛡️": 34, "Physicality 💪": 70},
    "Lallianzuala Chhangte (Mumbai City)": {"Pace ⚡": 86, "Shooting 🎯": 76, "Passing 🪄": 78, "Dribbling 🕺": 84, "Defending 🛡️": 48, "Physicality 💪": 68},
    "Dimitrios Diamantakos (ISL)": {"Pace ⚡": 78, "Shooting 🎯": 85, "Passing 🪄": 70, "Dribbling 🕺": 76, "Defending 🛡️": 40, "Physicality 💪": 82}
}

class PlayersStatsManager:
    """Manages top scorers, assists, and player performance radar data."""

    @staticmethod
    def get_top_scorers_df(league_name: str) -> pd.DataFrame:
        data = PLAYERS_LEADERBOARD.get(league_name, PLAYERS_LEADERBOARD["English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿"])
        return pd.DataFrame(data.get("top_scorers", []))

    @staticmethod
    def get_top_assists_df(league_name: str) -> pd.DataFrame:
        data = PLAYERS_LEADERBOARD.get(league_name, PLAYERS_LEADERBOARD["English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿"])
        return pd.DataFrame(data.get("top_assists", []))

    @staticmethod
    def get_radar_players() -> List[str]:
        return list(PLAYER_RADAR_PROFILES.keys())

    @staticmethod
    def get_player_radar_metrics(player_name: str) -> Dict[str, int]:
        return PLAYER_RADAR_PROFILES.get(player_name, PLAYER_RADAR_PROFILES["Kylian Mbappé (Real Madrid)"])
