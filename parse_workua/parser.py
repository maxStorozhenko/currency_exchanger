import sqlite3

import requests

from bs4 import BeautifulSoup

from fake_useragent import UserAgent


BASE_URL = 'https://www.work.ua/jobs/'
ua = UserAgent()
conn = sqlite3.connect('work_ua.db')

c = conn.cursor()

page = 0

while True:
    page += 1

    print(f'start parsing page: {page}')

    headers = {'User-Agent': ua.random}

    response = requests.get(BASE_URL, params={'page': page}, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    res = soup.find('div', {'id': 'pjax-job-list'})

    if res is None:
        break

    res = res.find_all('h2')

    number = 0
    for elem in res:
        number += 1
        print(f'page: {page}, vacancy: {number}')
        href = elem.find('a').attrs['href']
        vacancy_url = 'https://work.ua' + href
        vacancy_html = requests.get(vacancy_url)

        vacancy_soup = BeautifulSoup(vacancy_html.text, 'html.parser')

        # get date
        res = vacancy_soup.find('p', {'class': 'cut-bottom-print'})
        if res is not None and '<span class="label label-hot">Гаряча вакансія</span>' not in str(res):
            date = str(res.contents[1].string)
        else:
            date = '-'

        # get name
        res = vacancy_soup.find('h1', {'id': 'h1-name'})
        name = str(res.string)

        # get salary
        res = vacancy_soup.find('b', {'class': 'text-black'})
        if res is not None:
            salary = str(res.string)
        else:
            salary = '-'

        # get city
        res = vacancy_soup.find('p', {'class': 'text-indent add-top-sm'})
        city = res.contents[2].strip()

        # get description
        res = vacancy_soup.find('div', {'id': 'job-description'})
        description = res.text

        c.execute('''INSERT INTO vacancy VALUES (?, ?, ?, ?, ?)''', (date, name, salary, city, description))

    conn.commit()

conn.close()
