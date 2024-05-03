'''
<h3 class='bloko-header-section-3'>
<a href="https://adsrv.hh.ru/click?b=975574&amp;place=35&amp;meta=\
9BbUZYOAh0qHEJT6M6q5J8QcLFdeYZotVYoiayVx9WSNTl9O0R6JTemTpnNRoOi-EwAwgzHO6vzo\
TWHW1LF1YK6utIqMkoqcXkSPHAXb9TyrGJ41c9LbTUYcpgw6qRGLC47lFceB2yUJ3hYmsVvdgPawKEmPHiME08y_\
NIHmNYguJ-tZ1_sBF-oXJXKBPmw0LVc-HIc-5XMfEbqeJdpUVtJFVQAJjGnq9F4I68K3Qvh4F6KV8K4jbVEY5Z68_\
7kz4zoRcIRPCjEhSr1LaGd8c-X9W4yoj_OqPl-ttOVKzp6MimmmZKIknSjzBhbIiiWl39f9Y5zOw98u6cwReEOjOdgOPMTMQd_8oMPuVRamWPYve7\
LpxsFf4kzK9DQjoAjpJdWFJ0ksAkRINvkjw18Gbqxx2JiojXHVw8QoVbSqhp6lY4i_X95dh8NYneyIvwlaEcurDoMfQ7rL4-\
mz0wK3aqO7Ynwo5HNaooNeUS4SXw3TOKXY6QPXzkTURS0qHW9rIXs3nLYT1QDmIafO6IymA%3D%3D&amp;\
clickType=link_to_vacancy">

<div class="g-user-content" data-qa="vacancy-description"><p><span>
<div class = bloko-text>
<span data-qa='vacancy-salary-compensation-type-net'
'''
import json
import bs4
import requests
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_fake_headers())
main_page_data = bs4.BeautifulSoup(response.text, features='lxml')
articles_tag = main_page_data.findAll('div', class_='vacancy-serp-item__layout')

parsed_data = []

for article_tag in articles_tag:
    h3_tag = article_tag.find('h3', class_='bloko-header-section-3')
    a_tag = h3_tag.find('a')
    link = a_tag['href']
    title = a_tag.find('span').text.strip()
    article_response = requests.get(link, headers=get_fake_headers())
    article_data = bs4.BeautifulSoup(article_response.text, features='lxml')
    article_text = article_data.find('div', class_='g-user-content')
    salary = article_data.find('span', {'data-qa':'vacancy-serp__vacancy-compensation'})
    if salary == None:
        salary_vacancy = "Вакансия без зарплаты"
    else:
        salary_vacancy = salary.text
    a2_tag = article_tag.find('div', class_='vacancy-serp-item-body__main-info')
    name_tag = article_tag.find('div', class_='vacancy-serp-item__meta-info-company')
    company_name_tag = name_tag.find('a')
    company_name = company_name_tag.text
    location = a2_tag.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text.strip()
    if ',' in location:
        city = location.split(',')[0]
    else:
        city = location
    if 'Django' in article_text.text or 'Flask' in article_text.text:
        parsed_data.append({
            'link': link,
            'job title': title,
            'salary': salary_vacancy,
            'name company': company_name,
            'city': city,
        })


with open('vacancy_django_flask', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=1))





