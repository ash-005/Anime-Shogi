
import json
import pandas as pd
import os

DATA_DIR = "data"
AIRING_PATH = os.path.join(DATA_DIR, "anime_airing_1000.json")
NONAIRING_PATH = os.path.join(DATA_DIR, "anime_nonairing_1000.json")
ALLTIME_PATH = os.path.join(DATA_DIR, "anime_top_alltime.json")

def extract_genre_names(genres):
    if not genres:
        return []
    return [g["name"] for g in genres]

def load_and_flatten(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for entry in data:
        node = entry.get("node", {})
        node = node.copy()
        node["genres"] = extract_genre_names(node.get("genres"))
        records.append(node)
    return pd.DataFrame(records)

def main():
    df_airing = load_and_flatten(AIRING_PATH)
    df_nonairing = load_and_flatten(NONAIRING_PATH)
    df_alltime = load_and_flatten(ALLTIME_PATH)

    df_airing.to_csv(os.path.join(DATA_DIR, "anime_airing_1000_preprocessed.csv"), index=False)
    df_nonairing.to_csv(os.path.join(DATA_DIR, "anime_nonairing_1000_preprocessed.csv"), index=False)
    df_alltime.to_csv(os.path.join(DATA_DIR, "anime_alltime_preprocessed.csv"), index=False)
    print("Preprocessing complete. CSVs saved in data/ directory.")

if __name__ == "__main__":
    main()
