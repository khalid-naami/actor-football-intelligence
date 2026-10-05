"""Live Football Fixtures, Matches Engine & Real-Time Score Center.

Provides live match states, simulated live commentary/events, expected goals (xG),
possession percentages, shots on target, and scheduled fixtures across leagues.
"""

from typing import Dict, List, Any
import datetime
import random

LEAGUES_MATCHES: Dict[str, List[Dict[str, Any]]] = {
    "English Premier League 🏴󠁧󠁢󠁥󠁮󠁧󠁿": [
        {
            "id": "EPL-M1",
            "home_team": "Manchester City",
            "away_team": "Arsenal",
            "status": "LIVE",
            "minute": "74'",
            "score_home": 2,
            "score_away": 2,
            "xg_home": 2.14,
            "xg_away": 1.88,
            "possession_home": 62,
            "possession_away": 38,
            "shots_home": 16,
            "shots_away": 9,
            "stadium": "Etihad Stadium, Manchester (Capacity: 53,400)",
            "referee": "Michael Oliver",
            "events": ["9' Haaland (1-0)", "22' Calafiori (1-1)", "45+8' Gabriel (1-2)", "90+8' Stones (2-2)"]
        },
        {
            "id": "EPL-M2",
            "home_team": "Liverpool",
            "away_team": "Chelsea",
            "status": "FT",
            "minute": "Full Time",
            "score_home": 2,
            "score_away": 1,
            "xg_home": 1.95,
            "xg_away": 1.10,
            "possession_home": 54,
            "possession_away": 46,
            "shots_home": 14,
            "shots_away": 10,
            "stadium": "Anfield, Liverpool (Capacity: 61,276)",
            "referee": "John Brooks",
            "events": ["29' Salah (Pen 1-0)", "48' Jackson (1-1)", "51' Jones (2-1)"]
        },
        {
            "id": "EPL-M3",
            "home_team": "Tottenham Hotspur",
            "away_team": "Aston Villa",
            "status": "UPCOMING",
            "minute": "Tomorrow 17:30 UTC",
            "score_home": "-",
            "score_away": "-",
            "xg_home": 0.0,
            "xg_away": 0.0,
            "possession_home": 50,
            "possession_away": 50,
            "shots_home": 0,
            "shots_away": 0,
            "stadium": "Tottenham Hotspur Stadium, London (Capacity: 62,850)",
            "referee": "Craig Pawson",
            "events": []
        }
    ],

    "Spanish La Liga 🇪🇸": [
        {
            "id": "LAL-M1",
            "home_team": "Real Madrid",
            "away_team": "FC Barcelona",
            "status": "LIVE",
            "minute": "68'",
            "score_home": 1,
            "score_away": 2,
            "xg_home": 1.65,
            "xg_away": 2.30,
            "possession_home": 44,
            "possession_away": 56,
            "shots_home": 11,
            "shots_away": 15,
            "stadium": "Santiago Bernabéu, Madrid (Capacity: 84,744)",
            "referee": "José María Sánchez Martínez",
            "events": ["54' Lewandowski (0-1)", "56' Lewandowski (0-2)", "77' Lamine Yamal (0-3)", "84' Raphinha (0-4)"]
        },
        {
            "id": "LAL-M2",
            "home_team": "Atlético Madrid",
            "away_team": "Girona FC",
            "status": "FT",
            "minute": "Full Time",
            "score_home": 3,
            "score_away": 0,
            "xg_home": 2.40,
            "xg_away": 0.65,
            "possession_home": 48,
            "possession_away": 52,
            "shots_home": 17,
            "shots_away": 7,
            "stadium": "Cívitas Metropolitano, Madrid (Capacity: 70,460)",
            "referee": "Juan Martínez Munuera",
            "events": ["39' Griezmann (1-0)", "48' Llorente (2-0)", "90+4' Koke (3-0)"]
        }
    ],

    "Indian Super League (ISL) 🇮🇳": [
        {
            "id": "ISL-M1",
            "home_team": "Mohun Bagan Super Giant",
            "away_team": "Mumbai City FC",
            "status": "LIVE",
            "minute": "82'",
            "score_home": 2,
            "score_away": 1,
            "xg_home": 1.78,
            "xg_away": 1.45,
            "possession_home": 52,
            "possession_away": 48,
            "shots_home": 13,
            "shots_away": 11,
            "stadium": "Salt Lake Stadium (Vivekananda Yuba Bharati Krirangan), Kolkata (Capacity: 85,000)",
            "referee": "Tejas Nagvenkar",
            "events": ["28' Liston Colaco (1-0)", "44' Jason Cummings (2-0)", "69' Lallianzuala Chhangte (2-1)"]
        },
        {
            "id": "ISL-M2",
            "home_team": "Kerala Blasters FC",
            "away_team": "FC Goa",
            "status": "FT",
            "minute": "Full Time",
            "score_home": 4,
            "score_away": 2,
            "xg_home": 2.65,
            "xg_away": 1.90,
            "possession_home": 49,
            "possession_away": 51,
            "shots_home": 15,
            "shots_away": 12,
            "stadium": "Jawaharlal Nehru International Stadium, Kochi (Capacity: 41,143)",
            "referee": "Rahul Kumar Gupta",
            "events": ["7' Rowllin Borges (0-1)", "17' Mohammad Yasir (0-2)", "51' Daisuke Sakai (1-2)", "81' Diamantakos (2-2)", "84' Diamantakos (3-2)", "88' Fedor Černych (4-2)"]
        },
        {
            "id": "ISL-M3",
            "home_team": "East Bengal FC",
            "away_team": "Bengaluru FC",
            "status": "UPCOMING",
            "minute": "Sunday 14:00 UTC",
            "score_home": "-",
            "score_away": "-",
            "xg_home": 0.0,
            "xg_away": 0.0,
            "possession_home": 50,
            "possession_away": 50,
            "shots_home": 0,
            "shots_away": 0,
            "stadium": "Kalyani Stadium, West Bengal",
            "referee": "Pratik Mondal",
            "events": []
        }
    ],

    "UEFA Champions League 🏆": [
        {
            "id": "UCL-M1",
            "home_team": "Real Madrid",
            "away_team": "Borussia Dortmund",
            "status": "FT",
            "minute": "Full Time",
            "score_home": 5,
            "score_away": 2,
            "xg_home": 3.85,
            "xg_away": 1.70,
            "possession_home": 58,
            "possession_away": 42,
            "shots_home": 22,
            "shots_away": 9,
            "stadium": "Santiago Bernabéu, Madrid",
            "referee": "István Kovács",
            "events": ["30' Malen (0-1)", "34' Gittens (0-2)", "60' Rüdiger (1-2)", "62' Vinícius Júnior (2-2)", "83' Lucas Vázquez (3-2)", "86' Vinícius Júnior (4-2)", "90+3' Vinícius Júnior (Hat-trick 5-2)"]
        },
        {
            "id": "UCL-M2",
            "home_team": "FC Barcelona",
            "away_team": "Bayern Munich",
            "status": "FT",
            "minute": "Full Time",
            "score_home": 4,
            "score_away": 1,
            "xg_home": 2.10,
            "xg_away": 1.40,
            "possession_home": 40,
            "possession_away": 60,
            "shots_home": 12,
            "shots_away": 11,
            "stadium": "Estadi Olímpic Lluís Companys, Barcelona",
            "referee": "Slavko Vinčić",
            "events": ["1' Raphinha (1-0)", "18' Harry Kane (1-1)", "36' Lewandowski (2-1)", "45' Raphinha (3-1)", "56' Raphinha (Hat-trick 4-1)"]
        }
    ],

    "FIFA World Cup 2026 🌍": [
        {
            "id": "FWC-M1",
            "home_team": "Argentina 🇦🇷",
            "away_team": "France 🇫🇷",
            "status": "UPCOMING",
            "minute": "MetLife Stadium, New Jersey (Final)",
            "score_home": "-",
            "score_away": "-",
            "xg_home": 0.0,
            "xg_away": 0.0,
            "possession_home": 50,
            "possession_away": 50,
            "shots_home": 0,
            "shots_away": 0,
            "stadium": "MetLife Stadium, New York/New Jersey (Capacity: 82,500)",
            "referee": "Szymon Marciniak",
            "events": ["Head-to-Head Clash of Titans: Messi vs Mbappé 2026 Rematch Preview"]
        },
        {
            "id": "FWC-M2",
            "home_team": "Morocco 🇲🇦",
            "away_team": "Spain 🇪🇸",
            "status": "UPCOMING",
            "minute": "Azteca Stadium, Mexico City",
            "score_home": "-",
            "score_away": "-",
            "xg_home": 0.0,
            "xg_away": 0.0,
            "possession_home": 50,
            "possession_away": 50,
            "stadium": "Estadio Azteca, Mexico City (Capacity: 87,523)",
            "referee": "César Arturo Ramos",
            "events": []
        }
    ]
}

class MatchesEngine:
    """Manages fixtures, live scores, and match statistics."""

    @staticmethod
    def get_league_matches(league_name: str) -> List[Dict[str, Any]]:
        matches = LEAGUES_MATCHES.get(league_name, [])
        if not matches:
            # Generate realistic fixture set if generic
            return [
                {
                    "id": f"{league_name[:3]}-G1",
                    "home_team": "Top Seed A",
                    "away_team": "Challenger B",
                    "status": "LIVE",
                    "minute": "58'",
                    "score_home": 1,
                    "score_away": 0,
                    "xg_home": 1.45,
                    "xg_away": 0.85,
                    "possession_home": 55,
                    "possession_away": 45,
                    "shots_home": 10,
                    "shots_away": 6,
                    "stadium": "Main National Stadium",
                    "referee": "FIFA Elite Official",
                    "events": ["34' Goal (1-0)"]
                },
                {
                    "id": f"{league_name[:3]}-G2",
                    "home_team": "Contender C",
                    "away_team": "Contender D",
                    "status": "FT",
                    "minute": "Full Time",
                    "score_home": 2,
                    "score_away": 2,
                    "xg_home": 1.80,
                    "xg_away": 1.75,
                    "possession_home": 49,
                    "possession_away": 51,
                    "shots_home": 12,
                    "shots_away": 13,
                    "stadium": "City Arena",
                    "referee": "Senior Referee",
                    "events": ["12' (1-0)", "40' (1-1)", "70' (2-1)", "88' (2-2)"]
                }
            ]
        return matches
