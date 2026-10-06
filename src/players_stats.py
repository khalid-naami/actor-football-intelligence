"""Elite Player Statistics, Golden Boot Scorers & Playmaker Intelligence Engine.

Provides top goalscorers, assists leaders, clean sheets, market valuations,
and radar metrics across leagues (including Premier League, La Liga, ISL, UCL, etc.).
"""

from typing import Dict, List, Any
import pandas as pd

PLAYERS_LEADERBOARD: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿": {
        "top_scorers": [
            {"rank": 1, "player": "Erling Haaland", "team": "Manchester City", "goals": 10, "pens": 1, "matches": 7, "xg": 8.4, "mins_per_goal": 63},
            {"rank": 2, "player": "Cole Palmer", "team": "Chelsea", "goals": 6, "pens": 1, "matches": 7, "xg": 5.2, "mins_per_goal": 98},
            {"rank": 3, "player": "Luis Díaz", "team": "Liverpool", "goals": 5, "pens": 0, "matches": 7, "xg": 4.1, "mins_per_goal": 102},
            {"rank": 4, "player": "Bryan Mbeumo", "team": "Brentford", "goals": 5, "pens": 1, "matches": 7, "xg": 3.8, "mins_per_goal": 124},
            {"rank": 5, "player": "Mohamed Salah", "team": "Liverpool", "goals": 4, "pens": 1, "matches": 7, "xg": 4.5, "mins_per_goal": 145},
            {"rank": 6, "player": "Ollie Watkins", "team": "Aston Villa", "goals": 4, "pens": 0, "matches": 7, "xg": 4.2, "mins_per_goal": 138}
        ],
        "top_assists": [
            {"rank": 1, "player": "Bukayo Saka", "team": "Arsenal", "assists": 7, "key_passes": 28, "big_chances_created": 9},
            {"rank": 2, "player": "Cole Palmer", "team": "Chelsea", "assists": 4, "key_passes": 22, "big_chances_created": 7},
            {"rank": 3, "player": "Mohamed Salah", "team": "Liverpool", "assists": 4, "key_passes": 19, "big_chances_created": 6},
            {"rank": 4, "player": "James Maddison", "team": "Tottenham Hotspur", "assists": 3, "key_passes": 18, "big_chances_created": 5}
        ]
    },

    "Spanish La Liga 🇪🇸": {
        "top_scorers": [
            {"rank": 1, "player": "Robert Lewandowski", "team": "FC Barcelona", "goals": 10, "pens": 2, "matches": 9, "xg": 8.9, "mins_per_goal": 76},
            {"rank": 2, "player": "Ayoze Pérez", "team": "Villarreal", "goals": 6, "pens": 0, "matches": 7, "xg": 4.8, "mins_per_goal": 92},
            {"rank": 3, "player": "Raphinha", "team": "FC Barcelona", "goals": 5, "pens": 0, "matches": 9, "xg": 5.1, "mins_per_goal": 142},
            {"rank": 4, "player": "Kylian Mbappé", "team": "Real Madrid", "goals": 5, "pens": 3, "matches": 8, "xg": 6.2, "mins_per_goal": 136},
            {"rank": 5, "player": "Giovani Lo Celso", "team": "Real Betis", "goals": 5, "pens": 1, "matches": 6, "xg": 3.7, "mins_per_goal": 98},
            {"rank": 6, "player": "Lamine Yamal", "team": "FC Barcelona", "goals": 4, "pens": 0, "matches": 9, "xg": 3.4, "mins_per_goal": 184}
        ],
        "top_assists": [
            {"rank": 1, "player": "Lamine Yamal", "team": "FC Barcelona", "assists": 5, "key_passes": 24, "big_chances_created": 8},
            {"rank": 2, "player": "Raphinha", "team": "FC Barcelona", "assists": 4, "key_passes": 29, "big_chances_created": 9},
            {"rank": 3, "player": "Vinícius Júnior", "team": "Real Madrid", "assists": 4, "key_passes": 21, "big_chances_created": 7},
            {"rank": 4, "player": "Álex Baena", "team": "Villarreal", "assists": 4, "key_passes": 20, "big_chances_created": 6}
        ]
    },

    "German Bundesliga 🇩🇪": {
        "top_scorers": [
            {"rank": 1, "player": "Omar Marmoush", "team": "Eintracht Frankfurt", "goals": 8, "pens": 1, "matches": 6, "xg": 5.8, "mins_per_goal": 64},
            {"rank": 2, "player": "Harry Kane", "team": "Bayern Munich", "goals": 5, "pens": 2, "matches": 6, "xg": 5.2, "mins_per_goal": 94},
            {"rank": 3, "player": "Jonathan Burkardt", "team": "FSV Mainz 05", "goals": 5, "pens": 0, "matches": 6, "xg": 4.1, "mins_per_goal": 105},
            {"rank": 4, "player": "Victor Boniface", "team": "Bayer Leverkusen", "goals": 4, "pens": 0, "matches": 6, "xg": 4.6, "mins_per_goal": 112}
        ],
        "top_assists": [
            {"rank": 1, "player": "Harry Kane", "team": "Bayern Munich", "assists": 5, "key_passes": 16, "big_chances_created": 6},
            {"rank": 2, "player": "Omar Marmoush", "team": "Eintracht Frankfurt", "assists": 4, "key_passes": 18, "big_chances_created": 5},
            {"rank": 3, "player": "Florian Wirtz", "team": "Bayer Leverkusen", "assists": 3, "key_passes": 20, "big_chances_created": 5}
        ]
    },

    "Italian Serie A 🇮🇹": {
        "top_scorers": [
            {"rank": 1, "player": "Mateo Retegui", "team": "Atalanta", "goals": 7, "pens": 2, "matches": 7, "xg": 5.9, "mins_per_goal": 78},
            {"rank": 2, "player": "Marcus Thuram", "team": "Inter Milan", "goals": 7, "pens": 0, "matches": 7, "xg": 6.1, "mins_per_goal": 82},
            {"rank": 3, "player": "Christian Pulisic", "team": "AC Milan", "goals": 5, "pens": 1, "matches": 7, "xg": 4.2, "mins_per_goal": 115},
            {"rank": 4, "player": "Dušan Vlahović", "team": "Juventus", "goals": 5, "pens": 2, "matches": 7, "xg": 4.8, "mins_per_goal": 120}
        ],
        "top_assists": [
            {"rank": 1, "player": "Romelu Lukaku", "team": "Napoli", "assists": 4, "key_passes": 14, "big_chances_created": 5},
            {"rank": 2, "player": "Rafael Leão", "team": "AC Milan", "assists": 3, "key_passes": 17, "big_chances_created": 6},
            {"rank": 3, "player": "Ademola Lookman", "team": "Atalanta", "assists": 3, "key_passes": 15, "big_chances_created": 4}
        ]
    },

    "Saudi Pro League 🇸🇦": {
        "top_scorers": [
            {"rank": 1, "player": "Aleksandar Mitrović", "team": "Al Hilal", "goals": 9, "pens": 2, "matches": 6, "xg": 8.1, "mins_per_goal": 60},
            {"rank": 2, "player": "Karim Benzema", "team": "Al Ittihad", "goals": 7, "pens": 0, "matches": 6, "xg": 5.8, "mins_per_goal": 77},
            {"rank": 3, "player": "Cristiano Ronaldo", "team": "Al Nassr", "goals": 5, "pens": 2, "matches": 6, "xg": 5.2, "mins_per_goal": 108},
            {"rank": 4, "player": "Houssem Aouar", "team": "Al Ittihad", "goals": 5, "pens": 0, "matches": 6, "xg": 3.9, "mins_per_goal": 105}
        ],
        "top_assists": [
            {"rank": 1, "player": "Moussa Diaby", "team": "Al Ittihad", "assists": 7, "key_passes": 22, "big_chances_created": 8},
            {"rank": 2, "player": "Sadio Mané", "team": "Al Nassr", "assists": 5, "key_passes": 18, "big_chances_created": 6},
            {"rank": 3, "player": "Rúben Neves", "team": "Al Hilal", "assists": 4, "key_passes": 19, "big_chances_created": 5}
        ]
    },

    "UEFA Champions League 🏆": {
        "top_scorers": [
            {"rank": 1, "player": "Harry Kane", "team": "Bayern Munich", "goals": 4, "pens": 3, "matches": 2, "xg": 3.8, "mins_per_goal": 45},
            {"rank": 2, "player": "Serhou Guirassy", "team": "Borussia Dortmund", "goals": 3, "pens": 1, "matches": 2, "xg": 2.7, "mins_per_goal": 58},
            {"rank": 3, "player": "Karim Adeyemi", "team": "Borussia Dortmund", "goals": 3, "pens": 0, "matches": 2, "xg": 2.1, "mins_per_goal": 52},
            {"rank": 4, "player": "Abdallah Sima", "team": "Brest", "goals": 3, "pens": 0, "matches": 2, "xg": 1.9, "mins_per_goal": 59}
        ],
        "top_assists": [
            {"rank": 1, "player": "Joshua Kimmich", "team": "Bayern Munich", "assists": 3, "key_passes": 9, "big_chances_created": 4},
            {"rank": 2, "player": "Vinícius Júnior", "team": "Real Madrid", "assists": 2, "key_passes": 8, "big_chances_created": 3}
        ]
    },

    "Indian Super League (ISL) 🇮🇳": {
        "top_scorers": [
            {"rank": 1, "player": "Alaaeddine Ajaraie", "team": "NorthEast United FC", "goals": 5, "pens": 0, "matches": 4, "xg": 3.8, "mins_per_goal": 70},
            {"rank": 2, "player": "Armando Sadiku", "team": "FC Goa", "goals": 4, "pens": 1, "matches": 4, "xg": 3.2, "mins_per_goal": 85},
            {"rank": 3, "player": "Sunil Chhetri", "team": "Bengaluru FC", "goals": 3, "pens": 1, "matches": 4, "xg": 2.4, "mins_per_goal": 68}
        ],
        "top_assists": [
            {"rank": 1, "player": "Madih Talal", "team": "East Bengal FC", "assists": 3, "key_passes": 14, "big_chances_created": 4},
            {"rank": 2, "player": "Alberto Noguera", "team": "Bengaluru FC", "assists": 2, "key_passes": 11, "big_chances_created": 3}
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
