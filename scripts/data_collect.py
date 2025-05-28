import requests
import json
import time

client_id = "a155f0565eb99aa0b4a14e461e07bcdd"

headers = {
    "X-MAL-CLIENT-ID": client_id
}

# Step 1: Get top 100 airing anime with genres and useful fields
params = {
    "ranking_type": "airing",
    "limit": 100,
    "fields": "id,title,main_picture,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,start_date,end_date,media_type,status,genres"
}

response = requests.get(
    "https://api.myanimelist.net/v2/anime/ranking",
    headers=headers,
    params=params
)

print("Ranking response:", response.status_code)
if response.status_code != 200:
    print("Error:", response.text)
    exit(1)

data = response.json()
anime_list = data.get("data", [])

# Optional: Fetch more details for each anime (uncomment if needed)
# detailed_anime_list = []
# for entry in anime_list:
#     anime_id = entry["node"]["id"]
#     anime_url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
#     detail_params = {
#         "fields": "id,title,main_picture,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,start_date,end_date,media_type,status,genres"
#     }
#     detail_response = requests.get(anime_url, headers=headers, params=detail_params)
#     print(f"Fetched details for anime ID {anime_id}: {detail_response.status_code}")
#     if detail_response.status_code == 200:
#         detailed_anime_list.append(detail_response.json())
#     else:
#         print("Error fetching details:", detail_response.text)
#     time.sleep(0.6)  # Respect rate limit
# # Save detailed data
# with open('anime_data.json', 'w', encoding='utf-8') as f:
#     json.dump(detailed_anime_list, f, indent=4, ensure_ascii=False)
# print("Detailed anime data saved to anime_data.json")

# Save the ranking data (with genres)
with open('anime_data.json', 'w', encoding='utf-8') as f:
    json.dump(anime_list, f, indent=4, ensure_ascii=False)
print("Top airing anime with genres saved to anime_data.json")

# Fetch all-time top rated anime
params_top = {
    "ranking_type": "all",
    "limit": 100,
    "fields": "id,title,main_picture,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,start_date,end_date,media_type,status,genres"
}
response_top = requests.get(
    "https://api.myanimelist.net/v2/anime/ranking",
    headers=headers,
    params=params_top
)
print("All-time ranking response:", response_top.status_code)
if response_top.status_code == 200:
    data_top = response_top.json()
    anime_list_top = data_top.get("data", [])
    with open('anime_top_alltime.json', 'w', encoding='utf-8') as f:
        json.dump(anime_list_top, f, indent=4, ensure_ascii=False)
    print("All-time top rated anime saved to anime_top_alltime.json")
else:
    print("Error fetching all-time top rated anime:", response_top.text)