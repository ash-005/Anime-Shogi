# **Anime Shogi**


An interactive web application for anime analytics, genre impact studies, and personalized recommendations, powered by MyAnimeList data, Gemini AI, and advanced data science techniques. Built with Streamlit for easy deployment and a modern UI.

  

## Features

  

### 1. Anime Recommendation System

- **Content-Based Filtering:** Recommends anime based on user-selected titles and their features (genres, synopsis, etc.).

- **Collaborative Filtering:** Suggests anime using user-based similarity and collaborative patterns.

- **Gemini AI Fallback:** If no recommendations are found, Gemini AI provides intelligent suggestions.

  

### 2. Genre Impact Study Dashboard

- **Interactive Analytics:** Explore how genres impact anime scores, popularity, user count, and rank.

- **Plotly Visualizations:** Dynamic bar and scatter plots with metric selectors for deep analysis.

- **Filters:** Filter by minimum score, popularity, media type, and status.

- **Export:** Download genre metrics as CSV for further analysis.

  

### 3. Gemini-Powered Anime Chat Assistant

- **Conversational AI:** Chat with Gemini about anime, get recommendations, discuss characters, and more.

- **Context & Memory:** The assistant remembers your conversation for more relevant responses.

  

## Project Structure

  

```

├── app.py                      # Main Streamlit app

├── requirements.txt            # Python dependencies

├── README.md                   # Project documentation

├── data/                       # Datasets and model files

│   ├── anime_airing_1000_preprocessed.csv

│   ├── anime_alltime_preprocessed.csv

│   └── ...

├── scripts/                    # Data and analytics scripts

│   ├── data_collect.py         # MyAnimeList data collection

│   ├── data_preprocess.py      # Data cleaning and preprocessing

│   ├── anime_recommender.py    # Recommendation logic

│   └── genre_impact_study.py   # Genre analytics and plots

└── .streamlit/                 # (Optional) Streamlit config

```

  

## Setup & Deployment

  

### 1. Prerequisites

- Python 3.8+

- [Streamlit Community Cloud](https://streamlit.io/cloud) account (for deployment)

  

### 2. Installation

```bash

# Clone the repository

$ git clone <your-repo-url>

$ cd lazydev

  

# Install dependencies

$ pip install -r requirements.txt

```

  

### 3. Running Locally

```bash

streamlit run app.py

```

  

### 4. Deployment (Streamlit Community Cloud)

1. Push your code to a public GitHub repository.

2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and create a new app from your repo.

3. Add any required secrets (e.g., Gemini API keys) via the Streamlit Cloud UI.

4. (Optional) Customize `.streamlit/config.toml` for theming.

  

## Data Sources

- **MyAnimeList:** Top 1000 airing, non-airing, and all-time anime, including genres, scores, popularity, user counts, and more.

- Data is collected and preprocessed using scripts in the `scripts/` directory.

  

## Customization & Extensibility

- Add new analytics or plots in `scripts/genre_impact_study.py` and integrate them in `app.py`.

- Update or retrain recommendation logic in `scripts/anime_recommender.py`.

- Extend Gemini AI prompts or memory logic in `app.py`.
