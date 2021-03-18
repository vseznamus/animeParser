import requests
from bs4 import BeautifulSoup

URL = 'https://jut.su'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 YaBrowser/21.2.3.100 Yowser/2.5 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_links_from_green(html):
    urls = []
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('a', class_='the_hildi')
    for a in items:
        urls.append(a['href'])
    return urls


def get_links_to_player(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('source', res='1080')
    return items[0]['src']


def parse():
    start = int(input('Скачать серии от (введите номер): ------>  '))
    end = int(input('Скачать серии до (введите номер): ------->   '))
    counter = start - 1
    for i in range(start - 1, end):
        html = get_html(URL + get_links_from_green(get_html(URL + '/one-piece/'))[i])
        if html.status_code == 200:
            link = get_links_to_player(html)
            bytes = requests.get(link, headers=HEADERS)
            counter += 1
            print(f'Скачивание {counter} серии... ')
            with open(f'{counter}.mp4', 'wb') as file:
                file.write(bytes.content)
        else:
            print("НЕТ ОТВЕТА ОТ СЕРВЕРА")


parse()
