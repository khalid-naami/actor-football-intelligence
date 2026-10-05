"""Head-to-Head (H2H) Analytics & Match Prediction Engine.

Calculates Expected Goals (xG), Win/Draw/Loss probabilities using bivariate
Poisson distributions, most probable scorelines, and Over/Under thresholds.
"""

from typing import Dict, Any, List
import math

class H2HPredictorEngine:
    """Computes predictive match probabilities and scoreline distributions."""

    @staticmethod
    def calculate_match_odds(
        home_team: str,
        away_team: str,
        home_attack_rating: float = 1.85,
        home_defense_rating: float = 1.05,
        away_attack_rating: float = 1.45,
        away_defense_rating: float = 1.25,
        home_advantage: float = 1.15
    ) -> Dict[str, Any]:
        """Calculates expected goals (xG) and Win/Draw/Loss probabilities."""
        
        # Expected Goals
        home_xg = home_attack_rating * away_defense_rating * home_advantage
        away_xg = away_attack_rating * home_defense_rating

        # Poisson probabilities for scores 0 to 5
        home_probs = [H2HPredictorEngine._poisson(home_xg, k) for k in range(6)]
        away_probs = [H2HPredictorEngine._poisson(away_xg, k) for k in range(6)]

        win_home = 0.0
        draw = 0.0
        win_away = 0.0
        over_2_5 = 0.0
        btts = 0.0

        score_matrix = {}

        for h in range(6):
            for a in range(6):
                p = home_probs[h] * away_probs[a]
                score_matrix[f"{h} - {a}"] = p

                if h > a: win_home += p
                elif h == a: draw += p
                else: win_away += p

                if (h + a) > 2.5: over_2_5 += p
                if h > 0 and a > 0: btts += p

        # Normalize probabilities
        total = win_home + draw + win_away
        p_home = round((win_home / total) * 100, 1)
        p_draw = round((draw / total) * 100, 1)
        p_away = round((win_away / total) * 100, 1)

        # Top 3 most likely scorelines
        sorted_scores = sorted(score_matrix.items(), key=lambda x: x[1], reverse=True)[:3]
        top_scores = [{"score": s[0], "prob": round(s[1] * 100, 1)} for s in sorted_scores]

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
            "home_win_prob": p_home,
            "draw_prob": p_draw,
            "away_win_prob": p_away,
            "over_2_5_prob": round(over_2_5 * 100, 1),
            "btts_prob": round(btts * 100, 1),
            "top_scorelines": top_scores
        }

    @staticmethod
    def _poisson(lambda_val: float, k: int) -> float:
        return (math.exp(-lambda_val) * (lambda_val ** k)) / math.factorial(k)
