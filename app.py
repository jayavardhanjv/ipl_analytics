import pandas as pd
import dash as d
from dash import html
from dash import dcc
from dash.dependencies import Input,Output
import plotly.graph_objects as go


df = pd.read_csv('https://raw.githubusercontent.com/jayavardhanjv/ipl_analytics/main/ipl_batting.csv')a
batting = df.copy()

df.dropna(inplace=True)
df.isna().sum()


rcb_players = df[df['Team']=='Royal Challengers Bangalore']
rcb_players = list(rcb_players['PLAYER'].unique())


batting_metrics_list = [
    "Runs",
    "HS",
    "Avg",
    "BF",
    "SR",
    "100",
    "50",
    "4s",
    "6s",
    "Mat",
    "Inns",
    "NO",
]


team_list = [
    "All Teams",
    "Sunrisers Hyderabad",
    "Kings Xi Punjab",
    "Mumbai Indians",
    "Delhi Capitals",
    "Kolkata Knight Riders",
    "Royal Challengers Bangalore",
    "Chennai Super Kings",
    "Rajasthan Royals",
]

app = d.Dash()
app.title ="IPL Analytics"
app._favicon = ""
app.layout = html.Div([
        html.H1("IPL ANALYSIS (2008-2019) - PES1PG21CA140",style={"font-size":"42px","text-align": "center"}),


        html.Div([html.P(f"Their were total of {len(rcb_players)} players during 2008-2019 ")], style={"font-size":"26px","height": "45px","text-align":"center","color":484848}),
        html.Div(
            [
                html.H2("Select RCB Players to compare total runs per Season", style={"text-align":"center"}),
                dcc.Dropdown(
                    id="select-player-ts",
                    options=[
                        {"label": player, "value": player}
                        for player in rcb_players
                    ],
                    value=[
                        "Virat Kohli","AB de Villiers","Moeen Ali"
                    ],
                    multi=True,
                ),
                dcc.Graph(id="players-runs-time-series"),
            ]
        ),

        # Season Records
        html.Div([], style={"height": "45px"}),
        html.Div([html.H2("All Season Records")], style={"text-align":"center"}),

        html.Div([
            html.Div([
                    html.Label("Select a Metric"),
                    dcc.Dropdown(
                        id="season-metric-selector",
                        options=[
                            {
                                "label": metric,
                                "value": metric,
                            }
                            for metric in batting_metrics_list
                        ],
                        value="Runs",
                    ),
                ],
                style={
                    "width": "25%",
                    "float": "left",
                    "padding-right": "25px",
                    "display": "inline-block",
                },
            ),


            html.Div(
                [
                    html.Label("Season"),
                    dcc.Dropdown(
                        id="season-year-selector",
                        options=[
                            {
                                "label": str(year),
                                "value": year,
                            }
                            for year in range(
                                2019, 2007, -1
                            )
                        ],
                        value=2019,
                    ),
                ],
                style={
                    "width": "25%",
                    "float": "middle",
                    "display": "inline-block",
                },
            )
        ],
        style={"display": "flex", "justify-content": "center"}),


        html.Div([dcc.Graph(id="season-graph")])

],style={
        "padding":"0px 35px"
    }
)

# update players runs per seasons
@app.callback(
    Output("players-runs-time-series", "figure"), [Input("select-player-ts", "value")]
)
def update_players_runs_ts(player_names):
    fig = go.Figure()
    for player in player_names:
        fig.add_trace(
            go.Scatter(
                x=df[df["PLAYER"] == player]["Season"],
                y=df[df["PLAYER"] == player]["Runs"],
                mode="lines",
                name=player,
            )
        )

    fig.update_layout(
        xaxis=dict(title="Season"),
        yaxis=dict(title="Runs"),
        height=550,
    )

    return fig



# Season records
@app.callback(
    Output("season-graph", "figure"),
    [
        Input("season-metric-selector", "value"),
        Input("season-year-selector", "value")
    ],
)
def update_batting_season_graph(metric, season):
    df = batting[batting["Season"] == season]
    df = df[df["Team"] == "Royal Challengers Bangalore"]
    df = df.sort_values(by=metric, ascending=True)
    top_15 = df[:15]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=top_15[metric],
            x=top_15["PLAYER"],
            orientation="v"
        )
    )
    fig.update_layout(
        title="Top 15 {} Players according to {} in the year {}".format("Royal Challengers Bangalore", metric, season),
        xaxis=dict(title="{}".format(metric),autorange="reversed"),
        yaxis=dict(),
        height=600,
    )
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
