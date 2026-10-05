# Apify Actor: Global Football Intelligence & Poisson H2H Predictor ⚽📊

A football analytics Actor covering top global leagues (Premier League, La Liga, Serie A, Bundesliga, Indian Super League - ISL, Saudi Pro League, Botola Pro, MLS), continental club cups (UEFA Champions League, CAF, AFC Elite), the FIFA World Cup 2026, and bivariate Poisson xG match prediction models.

---

## 🌟 Key Features

1. **Top 20 Global Competitions**: Detailed telemetry and standings for Premier League, La Liga, Indian Super League (ISL), Bundesliga, Ligue 1, Serie A, SPL, Botola Pro, MLS, UEFA Champions League, CAF Champions League, AFC Champions League Elite, and World Cup 2026.
2. **Real-Time Match Center & Fixtures**: Scores, minutes, expected goals ($xG$), possession percentages, shots on target, and match events.
3. **Player Statistics & Golden Boot Leaderboards**: Top scorers, assists leaders, key passes created, penalty conversions, and mins-per-goal ratios.
4. **Bivariate Poisson H2H Predictor**: Uses attacking/defending efficiency indices and home advantage coefficients to compute exact Win/Draw/Loss probabilities, Over/Under 2.5 goals, BTTS, and most likely scorelines (e.g. 2-1, 1-1, 3-1).

---

## 📥 Input Schema

| Field | Type | Default | Description |
|---|---|---|---|
| `selectedLeagues` | Array | 13 competitions | Filter specific leagues or fetch all supported competitions. |
| `includeStandings` | Boolean | `true` | Include league table points, GD, and form guide. |
| `includeFixturesAndLiveScores` | Boolean | `true` | Include live match events and upcoming fixtures. |
| `includeTopScorers` | Boolean | `true` | Include top goalscorer and assist leaderboards. |
| `simulateH2H` | Boolean | `true` | Calculate bivariate Poisson match probability simulation. |
| `simulateH2HHomeTeam` | String | `"Manchester City"` | Home club for H2H simulation. |
| `simulateH2HAwayTeam` | String | `"Arsenal"` | Away club for H2H simulation. |

---

## 📤 Output Dataset Format

```json
{
  "record_type": "h2h_poisson_prediction",
  "home_team": "Manchester City",
  "away_team": "Arsenal",
  "home_expected_goals_xg": 2.24,
  "away_expected_goals_xg": 1.52,
  "win_probability_home_pct": 52.8,
  "draw_probability_pct": 23.4,
  "win_probability_away_pct": 23.8,
  "over_2_5_goals_probability_pct": 68.2,
  "both_teams_to_score_btts_pct": 61.5,
  "most_likely_scorelines": [
    { "score": "2 - 1", "probability_pct": 11.4 },
    { "score": "2 - 2", "probability_pct": 8.7 },
    { "score": "1 - 1", "probability_pct": 8.1 }
  ]
}
```

---

## 🚀 How to Run Locally

```bash
cd actor-football-intelligence
pip install -r requirements.txt
python -m src.main
```
