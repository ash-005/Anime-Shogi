import requests
import json
import time
import os

client_id = "a155f0565eb99aa0b4a14e461e07bcdd"

headers = {
    "X-MAL-CLIENT-ID": client_id
}


all_anime = []
limit = 100
total = 1000
fields = "id,title,main_picture,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,start_date,end_date,media_type,status,genres"
next_url = "https://api.myanimelist.net/v2/anime/ranking"
params = {
    "ranking_type": "airing",
    "limit": limit,
    "fields": fields
}
count = 0
while next_url and count < total:
    response = requests.get(next_url, headers=headers, params=params if next_url.endswith("ranking") else None)
    print(f"Ranking response ({count+1}-{count+limit}):", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
        break
    data = response.json()
    anime_list = data.get("data", [])
    all_anime.extend(anime_list)
    count += len(anime_list)
    # Get next page URL
    next_url = data.get("paging", {}).get("next")
    params = None  # Only needed for first request
    time.sleep(0.6)  # Respect rate limit
    if not anime_list:
        break


os.makedirs('data', exist_ok=True)
with open('data/anime_airing_1000.json', 'w', encoding='utf-8') as f:
    json.dump(all_anime, f, indent=4, ensure_ascii=False)
print("Top 1000 airing anime with genres saved to data/anime_airing_1000.json")

all_nonairing = []
limit = 100
total = 1000
fields = "id,title,main_picture,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,start_date,end_date,media_type,status,genres"
next_url = "https://api.myanimelist.net/v2/anime/ranking"
params = {
    "ranking_type": "bypopularity",
    "limit": limit,
    "fields": fields
}
count = 0
while next_url and count < total:
    response = requests.get(next_url, headers=headers, params=params if next_url.endswith("ranking") else None)
    print(f"Non-airing response ({count+1}-{count+limit}):", response.status_code)
    if response.status_code != 200:
        print("Error:", response.text)
        break
    data = response.json()
    anime_list = data.get("data", [])
    # Filter: not currently airing and mean > 6
    for entry in anime_list:
        node = entry.get("node", {})
        if node.get("status") != "currently_airing" and node.get("mean", 0) > 6:
            all_nonairing.append(entry)
    count += len(anime_list)
    next_url = data.get("paging", {}).get("next")
    params = None
    time.sleep(0.6)
    if not anime_list:
        break

with open('data/anime_nonairing_1000.json', 'w', encoding='utf-8') as f:
    json.dump(all_nonairing[:1000], f, indent=4, ensure_ascii=False)
print("Top 1000 non-airing anime (mean > 6) saved to data/anime_nonairing_1000.json")
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


# (Remove old save for anime_data.json, as anime_list may be unbound)

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