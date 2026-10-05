"""Interactive Football Analytics & Match Visualizations with Plotly.

Generates player radar charts, xG momentum bars, win probability donuts,
and league goal-difference distribution charts.
"""

from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

CHART_THEME = {
    "paper_bgcolor": "rgba(15, 23, 42, 0.0)",
    "plot_bgcolor": "rgba(15, 23, 42, 0.0)",
    "font_color": "#e2e8f0",
    "grid_color": "rgba(148, 163, 184, 0.15)"
}

def create_player_radar_chart(player_name: str, metrics: Dict[str, int]) -> go.Figure:
    """Creates a 6-axis polar radar chart for player performance attributes."""
    categories = list(metrics.keys())
    values = list(metrics.values())

    # Close the radar loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.35)',
        line=dict(color='#38bdf8', width=2.5),
        marker=dict(size=7, color='#f59e0b'),
        name=player_name
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickcolor="#94a3b8", gridcolor=CHART_THEME["grid_color"]),
            angularaxis=dict(tickcolor="#f8fafc", gridcolor=CHART_THEME["grid_color"])
        ),
        title=dict(text=f"<b>Attribute Radar Profile:</b> {player_name}", font=dict(color="#f8fafc", size=15)),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        margin=dict(l=40, r=40, t=50, b=30),
        height=340
    )
    return fig

def create_match_prediction_donut(home_team: str, away_team: str, p_home: float, p_draw: float, p_away: float) -> go.Figure:
    """Creates a 3-way win/draw/loss probability distribution donut."""
    labels = [f"{home_team} Win", "Draw 🤝", f"{away_team} Win"]
    values = [p_home, p_draw, p_away]
    colors = ["#10b981", "#94a3b8", "#38bdf8"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color="#ffffff"),
        hoverinfo="label+value+percent"
    )])

    fig.update_layout(
        title=dict(text=f"<b>Match Outcome Probability</b><br><span style='font-size:12px; color:#94a3b8;'>{home_team} vs {away_team}</span>", font=dict(color="#f8fafc", size=15)),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        height=320
    )
    return fig

def create_standings_goal_diff_bar(df_standings: pd.DataFrame, league_title: str) -> go.Figure:
    """Bar chart of Goal Difference across teams in the league."""
    if df_standings.empty or "gd" not in df_standings.columns:
        return go.Figure()

    df_sorted = df_standings.sort_values(by="gd", ascending=True)
    colors = ["#10b981" if x > 0 else ("#ef4444" if x < 0 else "#94a3b8") for x in df_sorted["gd"]]

    fig = go.Figure(go.Bar(
        x=df_sorted["gd"],
        y=df_sorted["team"],
        orientation='h',
        marker=dict(color=colors, line=dict(color="#0f172a", width=1)),
        text=df_sorted["gd"],
        textposition="auto"
    ))

    fig.update_layout(
        title=dict(text=f"<b>Goal Difference (GD) Spectrum — {league_title}</b>", font=dict(color="#f8fafc", size=15)),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=dict(color=CHART_THEME["font_color"]),
        xaxis=dict(title="Goal Difference (GD)", gridcolor=CHART_THEME["grid_color"]),
        yaxis=dict(gridcolor=CHART_THEME["grid_color"]),
        margin=dict(l=120, r=20, t=50, b=40),
        height=400
    )
    return fig
