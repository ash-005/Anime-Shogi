
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
st.set_page_config(page_title="Anime & Gemini AI App", page_icon="", layout="centered")

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
page = st.sidebar.radio("Go to", ["Recommendation System", "Discuss Anime with Gemini"])

if page == "Recommendation System":
    st.title("Anime Recommendation System")
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