# Anime Recommendation System: Content-Based & Collaborative Filtering
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
import os
import joblib
import ast


DATA_DIR = "data"
AIRING_CSV = os.path.join(DATA_DIR, "anime_airing_preprocessed.csv")
ALLTIME_CSV = os.path.join(DATA_DIR, "anime_nonairing_1000_preprocessed.csv")
df = pd.read_csv(ALLTIME_CSV)

synopsis = df["synopsis"].fillna("")

## TF-IDF vectorizations on synopsis
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
tfidf_matrix = vectorizer.fit_transform(synopsis)



genres = df["genres"].fillna("[]").apply(ast.literal_eval)
mlb = MultiLabelBinarizer()
genre_matrix = mlb.fit_transform(genres)

## combining features
from scipy.sparse import hstack
features = hstack([tfidf_matrix, genre_matrix]).tocsr()

## cosine similarity for content-based recommendations
content_sim = cosine_similarity(features.toarray())


scaler = MinMaxScaler()
collab_features = scaler.fit_transform(df[["mean", "popularity"]].fillna(0))
collab_sim = cosine_similarity(collab_features)

def recommend_content_based(title, top_n=5):
    idx = df[df["title"].str.lower() == title.lower()].index
    if len(idx) == 0:
        print(f"Title '{title}' not found.")
        return []
    idx = idx[0]
    sim_scores = list(enumerate(content_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recs = [df.iloc[i]["title"] for i, score in sim_scores[1:top_n+1]]
    return recs

def recommend_collaborative(title, top_n=5):
    idx = df[df["title"].str.lower() == title.lower()].index
    if len(idx) == 0:
        print(f"Title '{title}' not found.")
        return []
    idx = idx[0]
    sim_scores = list(enumerate(collab_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recs = [df.iloc[i]["title"] for i, score in sim_scores[1:top_n+1]]
    return recs
def save_models():
    joblib.dump(vectorizer, "data/tfidf_vectorizer.joblib")
    joblib.dump(mlb, "data/genre_encoder.joblib")
    joblib.dump(features, "data/features_matrix.joblib")
    df.to_csv("data/anime_recommender_df.csv", index=False)
    print("Models saved successfully.")
if __name__ == "__main__":
    anime_title = input("Enter an anime title for recommendations: ")
    print("\nContent-based recommendations:")
    print(recommend_content_based(anime_title))
    print("\nCollaborative (score/popularity) recommendations:")
    print(recommend_collaborative(anime_title))
    save_models()