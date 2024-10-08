import requests
import csv

url_vac = 'https://api.hh.ru/vacancies'
url_areas = 'https://api.hh.ru/areas'

region_ids = []
response = requests.get(url_areas)
if response.status_code:
    response_data = response.json()
    obj_ru = next(data for data in response_data if data['name'] == 'Россия')
    rus = obj_ru['id']

page = 0
vacancies = []
while len(vacancies) < 1000:
    response_vac = requests.get(url_vac, params={'page': 0,
                                                 'per_page': 100,
                                                 'schedule': 'remote',
                                                 'text': 'NAME:Аналитик',
                                                 'experience': 'noExperience',
                                                 'area': 113,
                                                 'only_with_salary': True,
                                                 'accredited_it_employer': True})
    res = response_vac.json().get('items')
    if res:
        for vac in res:
            data = {'Вакансия': vac.get('name'),
                    'Компания': vac.get('employer').get('name'),
                    'Зарплата': vac.get('salary'),
                    'Сайт': vac.get('url')}
            vacancies.append(data)
            print(vacancies)
        page += 1
    else:
        break


if len(vacancies) > 0:
    for e in vacancies:
        print(e)

with open('Analysts.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = vacancies[0].keys()
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(vacancies)