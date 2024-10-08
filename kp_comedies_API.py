import requests
import json
from pprint import pprint

token = 'B1JRZ2R-T2B4GP6-MXE01SW-ZJPFTC4'
url = 'https://api.kinopoisk.dev/v1.4/movie'

res_comedies = []
# get first page
response = requests.get(url,
                        params={'type': ['movie'],
                                'genres.name': ['комедия'],
                                'year': ['2000'],
                                'selectFields': ['name', 'movieLength', 'countries', 'rating'],
                                'sortField': 'rating.kp',
                                'sortType': [-1],
                                'page': 1,
                                'limit': 250},
                        headers={'accept': 'application/json', 'X-API-KEY': token})
# get list of dicts
print(response)
if response.status_code:
    response_json = response.json()
    res_comedies += response_json.get('items', [])
    count_pages = response_json.get('pages', 0)
    for page in range(2, count_pages):
        response = requests.get(url,
                                params={'type': ['movie'],
                                        'genres.name': ['комедия'],
                                        'year': ['2000'],
                                        'selectFields': ['name', 'movieLength', 'countries', 'rating'],
                                        'sortField': 'rating.kp',
                                        'sortType': [-1],
                                        'page': page,
                                        'limit': 250},
                                headers={'accept': 'application/json', 'X-API-KEY': token})
        if response.status_code:
            res_comedies += response.json().get('docs', [])
            # if len(res_comedies) > 999:
            #     break
print(len(res_comedies))
# res_name = [i['name'] for i in res_comedies]
list_movies = []

for film in res_comedies:
    list_movies.append((film.get('name', None),
                        film.get('movieLength', None),
                        film.get('countries', None),
                        film.get('rating', None)))

# list_movies_sorted = sorted(list_movies, key=lambda x: x[3]['kp'])

print(len(list_movies))
for name in list_movies:
    print(name)

# with open('comedies_4.json', 'w', encoding='utf-8') as f:
#     json.dump(list_movies_sorted, f, ensure_ascii=False)

# with open('comedies_sorted.json', 'w', encoding='utf-8') as f:
#     json.dump(list_movies_sorted, f, ensure_ascii=False)
