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
    if len(items) == 0:
        return -1
    return items[0]['src']


def get_name(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all('span', itemprop='name')
    return items[0].text.replace('Смотреть ', '')


def get_data():
    anime_url = input('Введите ссылку на JUT.SU страницу аниме (например: https://jut.su/ao-no-exorcist/): ---> ')
    folder = str(input('Укажите путь, куда будет скачан файл (!!!скопируйте путь с проводника!!!): ---->   ')).replace(
        '\\', '/') + '/'
    start = int(input('Скачать серии от (введите порядковый номер): ------>  '))
    end = int(input('Скачать серии до (введите порядковый номер): ------->   '))
    return anime_url, folder, start, end


def parse(anime_url, folder, start, end):
    for i in range(start - 1, end):
        html = get_html(URL + get_links_from_green(get_html(anime_url))[i])
        print(f'Скачивание ' + '"' + get_name(html) + '"' + '...')
        if html.status_code == 200:
            if get_links_to_player(html) != -1:
                link = get_links_to_player(html)
                bytes = requests.get(link, headers=HEADERS)
                with open(folder + get_name(html) + '.mp4', 'wb') as file:
                    file.write(bytes.content)
                print("Скачивание " + get_name(html) + ' завершено')
            else:
                print('Невозможно скачать серию выше(')
                i += 1
        else:
            print("НЕТ ОТВЕТА ОТ СЕРВЕРА")


if __name__ == '__main__':
    url, f, s, e = get_data()
    parse(url, f, s, e)
