
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast

# --- CONFIG ---
DATA_PATH = "data/anime_airing_1000_preprocessed.csv"  # or anime_alltime_preprocessed.csv

# --- LOAD DATA ---
df = pd.read_csv(DATA_PATH)
df["genres"] = df["genres"].fillna("[]").apply(ast.literal_eval)
df_exploded = df.explode("genres")

# --- FILTERS ---
def filter_df(df, min_score=None, min_popularity=None, media_type=None, status=None):
    dff = df.copy()
    if min_score is not None:
        dff = dff[dff["mean"] >= min_score]
    if min_popularity is not None:
        dff = dff[dff["popularity"] >= min_popularity]
    if media_type:
        dff = dff[dff["media_type"] == media_type]
    if status:
        dff = dff[dff["status"] == status]
    return dff

# --- METRICS ---
def genre_metrics(dff):
    return dff.groupby("genres").agg(
        avg_score=("mean", "mean"),
        median_score=("mean", "median"),
        min_score=("mean", "min"),
        max_score=("mean", "max"),
        std_score=("mean", "std"),
        avg_popularity=("popularity", "mean"),
        median_popularity=("popularity", "median"),
        min_popularity=("popularity", "min"),
        max_popularity=("popularity", "max"),
        std_popularity=("popularity", "std"),
        count=("title", "count"),
        avg_users=("num_list_users", "mean"),
        median_users=("num_list_users", "median"),
        min_users=("num_list_users", "min"),
        max_users=("num_list_users", "max"),
        std_users=("num_list_users", "std"),
        avg_rank=("rank", "mean"),
        median_rank=("rank", "median"),
        min_rank=("rank", "min"),
        max_rank=("rank", "max"),
        std_rank=("rank", "std"),
    ).reset_index()

# --- INTERACTIVE PLOTS ---
def plot_genre_bar(df_metrics, y, title, color=None):
    fig = px.bar(
        df_metrics.sort_values(y, ascending=False),
        x="genres", y=y, color=color or y,
        title=title,
        labels={"genres": "Genre", y: y.replace("_", " ").title()},
        color_continuous_scale="Viridis"
    )
    fig.update_layout(xaxis_tickangle=-45, xaxis_title="Genre", yaxis_title=y.replace("_", " ").title())
    return fig

def plot_genre_scatter(df_metrics, x, y, size="count", title=None):
    fig = px.scatter(
        df_metrics, x=x, y=y, size=size, color="genres",
        hover_name="genres", title=title or f"{y} vs {x} by Genre"
    )
    return fig

if __name__ == "__main__":
    dff = filter_df(df_exploded, min_score=6, media_type="tv")
    metrics = genre_metrics(dff)

    fig1 = plot_genre_bar(metrics, y="avg_score", title="Average Mean Score by Genre")
    fig1.show()

    fig2 = plot_genre_bar(metrics, y="avg_popularity", title="Average Popularity by Genre")
    fig2.show()

    fig3 = plot_genre_scatter(metrics, x="avg_score", y="avg_popularity", size="count", title="Popularity vs Score by Genre")
    fig3.show()