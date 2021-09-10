import requests
from bs4 import BeautifulSoup
import csv
import os

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': '*/*'
}
HOST = 'https://kolesa.kz'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pager').findChildren('li')
    if pagination:
        return int(pagination[2].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='a-elem')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('span', class_='a-el-info-title').get_text(strip=True),
            'link': HOST + item.find('a', class_='ddl_product_link').get('href'),
            'price': item.find('span', class_='price').get_text(strip=True).replace(' ', ''),
            'city': item.find('div', class_='list-region').get_text(strip=True)
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-16') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['city']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        cars = []
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            # cars = get_content(html.text)
        save_file(cars, FILE)
        os.startfile(FILE)
        print(f'Всего {len(cars)} автомобилей')
    else:
        print('Error')


parse()
