
import streamlit as st
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import ast
import requests
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("api_key") or os.getenv("API_KEY")

# Load saved objects
df = pd.read_csv("data/anime_recommender_df.csv")
vectorizer = joblib.load("data/tfidf_vectorizer.joblib")
mlb = joblib.load("data/genre_encoder.joblib")
features = joblib.load("data/features_matrix.joblib")


def recommend(title, top_n=5):
    idx = df[df["title"].str.lower() == title.lower()].index
    if len(idx) == 0:
        return []
    idx = idx[0]
    sim_scores = list(enumerate(cosine_similarity(features[idx], features)[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recs = [df.iloc[i]["title"] for i, score in sim_scores[1:top_n+1]]
    return recs

def ask_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Gemini API key not found. Please set it in your .env file."
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    params = {"key": GEMINI_API_KEY}
    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Gemini error: {response.text}"
    except Exception as e:
        return f"Gemini request failed: {e}"




# --- Streamlit Sidebar Navigation ---
st.set_page_config(page_title="Anime Shogi", page_icon="🍥", layout="centered")

st.markdown("""
    <style>
    .main {background-color: #181825; color: #f3f3f3;}
    .stTextInput > div > div > input, .stTextArea textarea {
        background-color: #232339 !important; color: #f3f3f3 !important;
        border: 1px solid #44465a !important;
    }
    .stButton button {
        background-color: #3b3b5b; color: #f3f3f3; font-weight: bold;
    }
    .stSidebar {background-color: #232339;}
    .stMarkdown {font-size: 1.1em;}
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Recommendation System", "Genre Impact Study", "Discuss Anime with Gemini"])

if page == "Recommendation System":
    st.title("Home to your anime needs 🍥")
    st.markdown("""
    Enter an anime title to get recommendations based on content similarity. If the anime is not found, Gemini will try to help!
    """)
    anime_title = st.text_input("Enter an anime title:")
    if anime_title:
        recs = recommend(anime_title)
        if recs:
            st.write("Recommended Anime:")
            for r in recs:
                st.write(r)
        else:
            st.write("Title not found in database. Asking Gemini for recommendations...")
            gemini_prompt = f"Recommend some anime similar to '{anime_title}'."
            gemini_response = ask_gemini(gemini_prompt)
            st.write(gemini_response)

elif page == "Genre Impact Study":
    import plotly.express as px
    import plotly.graph_objects as go
    import ast
    st.title("Genre Impact Study")
    st.markdown("""
    Explore how different genres affect anime scores, popularity, and more. Use the filters below to customize your analysis.
    """)
    genre_data_file = st.selectbox("Select dataset", [
        "data/anime_airing_1000_preprocessed.csv",
        "data/anime_alltime_preprocessed.csv",
        "data/anime_nonairing_1000_preprocessed.csv"
    ], format_func=lambda x: x.split("/")[-1])
    df = pd.read_csv(genre_data_file)
    df["genres"] = df["genres"].fillna("[]").apply(ast.literal_eval)
    df_exploded = df.explode("genres")

    min_score = st.slider("Minimum Mean Score", float(df["mean"].min()), float(df["mean"].max()), 6.0, 0.1)
    min_popularity = st.slider("Minimum Popularity", float(df["popularity"].min()), float(df["popularity"].max()), float(df["popularity"].min()), 1.0)
    media_types = ["All"] + sorted(df["media_type"].dropna().unique().tolist())
    media_type = st.selectbox("Media Type", media_types)
    statuses = ["All"] + sorted(df["status"].dropna().unique().tolist())
    status = st.selectbox("Status", statuses)

    def filter_df(df, min_score=None, min_popularity=None, media_type=None, status=None):
        dff = df.copy()
        if min_score is not None:
            dff = dff[dff["mean"] >= min_score]
        if min_popularity is not None:
            dff = dff[dff["popularity"] >= min_popularity]
        if media_type and media_type != "All":
            dff = dff[dff["media_type"] == media_type]
        if status and status != "All":
            dff = dff[dff["status"] == status]
        return dff

    dff = filter_df(df_exploded, min_score, min_popularity, media_type, status)

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

    metrics = genre_metrics(dff)

    # --- Metric Selectors ---
    st.markdown("#### Select Metrics to Visualize")
    metric_options = {
        "Score": ["avg_score", "median_score", "min_score", "max_score", "std_score"],
        "Popularity": ["avg_popularity", "median_popularity", "min_popularity", "max_popularity", "std_popularity"],
        "Users": ["avg_users", "median_users", "min_users", "max_users", "std_users"],
        "Rank": ["avg_rank", "median_rank", "min_rank", "max_rank", "std_rank"]
    }
    metric_labels = {
        "avg_score": "Average Score",
        "median_score": "Median Score",
        "min_score": "Min Score",
        "max_score": "Max Score",
        "std_score": "Score StdDev",
        "avg_popularity": "Average Popularity",
        "median_popularity": "Median Popularity",
        "min_popularity": "Min Popularity",
        "max_popularity": "Max Popularity",
        "std_popularity": "Popularity StdDev",
        "avg_users": "Average Users",
        "median_users": "Median Users",
        "min_users": "Min Users",
        "max_users": "Max Users",
        "std_users": "Users StdDev",
        "avg_rank": "Average Rank",
        "median_rank": "Median Rank",
        "min_rank": "Min Rank",
        "max_rank": "Max Rank",
        "std_rank": "Rank StdDev"
    }

    col1, col2 = st.columns(2)
    with col1:
        bar_metric_group = st.selectbox("Bar Chart Metric Group", list(metric_options.keys()), index=0)
        bar_metric = st.selectbox("Bar Chart Metric", metric_options[bar_metric_group], format_func=lambda x: metric_labels[x], index=0)
    with col2:
        scatter_x_group = st.selectbox("Scatter X Metric Group", list(metric_options.keys()), index=0)
        scatter_x_metric = st.selectbox("Scatter X Metric", metric_options[scatter_x_group], format_func=lambda x: metric_labels[x], index=0)
        scatter_y_group = st.selectbox("Scatter Y Metric Group", list(metric_options.keys()), index=1)
        scatter_y_metric = st.selectbox("Scatter Y Metric", metric_options[scatter_y_group], format_func=lambda x: metric_labels[x], index=0)

    # --- Bar Chart ---
    st.markdown(f"#### {metric_labels[bar_metric]} by Genre")
    fig1 = px.bar(
        metrics.sort_values(bar_metric, ascending=False),
        x="genres", y=bar_metric, color=bar_metric,
        color_continuous_scale="Viridis",
        labels={"genres": "Genre", bar_metric: metric_labels[bar_metric]},
        title=f"{metric_labels[bar_metric]} by Genre"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

    # --- Scatter Chart ---
    st.markdown(f"#### {metric_labels[scatter_y_metric]} vs {metric_labels[scatter_x_metric]} by Genre")
    fig2 = px.scatter(
        metrics, x=scatter_x_metric, y=scatter_y_metric, size="count", color="genres",
        hover_name="genres", title=f"{metric_labels[scatter_y_metric]} vs {metric_labels[scatter_x_metric]} by Genre"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Download Option ---
    st.markdown("#### Download Genre Metrics")
    csv = metrics.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download genre metrics as CSV",
        data=csv,
        file_name="genre_metrics.csv",
        mime="text/csv"
    )

elif page == "Discuss Anime with Gemini":
    st.title(" Discuss Anime with Gemini AI")
    st.markdown("""
    Welcome to your anime chat assistant powered by Gemini! Ask anything about anime, get recommendations, discuss characters, or just have fun chatting. Your conversation is remembered for context.
    """)

    if "gemini_chat_history" not in st.session_state:
        st.session_state["gemini_chat_history"] = []

    def format_chat(history):
        return "\n".join([f"User: {q}\nGemini: {a}" for q, a in history])

    with st.form("gemini_chat_form", clear_on_submit=True):
        user_q = st.text_area("Type your message:", key="chat_input")
        submitted = st.form_submit_button("Send")
        if submitted and user_q:
            chat_context = format_chat(st.session_state["gemini_chat_history"])
            prompt = chat_context + ("\nUser: " + user_q if chat_context else user_q)
            gemini_response = ask_gemini(prompt)
            st.session_state["gemini_chat_history"].append((user_q, gemini_response))

    
    if st.session_state["gemini_chat_history"]:
        st.markdown("---")
        st.subheader("Chat History")
        for q, a in st.session_state["gemini_chat_history"][::-1]:
            st.markdown(f"<div style='background:#121211;padding:10px;border-radius:10px;margin-bottom:5px'><b>You:</b> {q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:#121211;padding:10px;border-radius:10px;margin-bottom:15px'><b>Gemini:</b> {a}</div>", unsafe_allow_html=True)