import requests
from bs4 import BeautifulSoup
import csv

MAX_PAGE = 2  # 14280
result = []
try:
    num = 1
    resp = requests.get('https://www.chitai-gorod.ru/catalog/books-18030', params={'page': 1, 'filters[categories]': 18030})
    bs = BeautifulSoup(resp.text, 'lxml')
    pagination_elements = bs.find_all('span', class_='pagination__text')
    max_page = 1
    if pagination_elements:
        max_page = int(pagination_elements[-1].get_text().strip())
        print(max_page)
    for page in range(MAX_PAGE + 1):
        resp = requests.get('https://www.chitai-gorod.ru/catalog/books-18030', params={'page': page})
        html = resp.text
        bs = BeautifulSoup(html, 'lxml')
        cards = bs.find_all('article', class_='product-card product-card product')  # find
        # print(cards)
        # for card in cards:
        #   print(card.get_text().strip())
        # cards_1 = bs.select_one('article.product-card')
        # print(cards_1.get_text())

        for card in cards:
            name = card.find('div', class_='product-title__head')
            if name:
                name = name.text.strip()
            else:
                name = ''
            # print(num, ':', name)
            # num += 1

            rating = card.find('meta', attrs={'itemprop': 'ratingValue'})
            if rating:
                rating = rating['content']  # content='rating' рейтинг в атрибуте контент
            else:
                rating = ''

            price = card.find('div', class_='product-price__value product-price__value--discount')
            if price:
                price = price.get_text().strip()
            else:
                price = ''

            result.append({'name': name, 'rating': rating, 'price': price})
            num += 1
    with open('task_books.csv', 'w', encoding='utf-8') as result_file:
        field_name = ['name', 'rating', 'price']
        writer = csv.DictWriter(result_file, fieldnames=field_name)
        writer.writeheader()
        for row in result:
            writer.writerow(row)

except Exception as ex:
    print(ex)

for r in result:
    print(r)