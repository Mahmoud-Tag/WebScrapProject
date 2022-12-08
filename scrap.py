# 1 First Step install and import modules
# --pip/pip3 install requests
# --pip/pip3 install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
job_skill = []
location_name = []
links = []
salary = []
responsibilities = []
date = []
page_num = 0

while True:
    # 2nd step use requests to fetch url
    try:
        result = requests.get(
            f'https://wuzzuf.net/search/jobs/?a=hpb%7Cspbg&q=python&start={page_num}')
        # 3rd step save page content/markup
        src = result.content
        # print (src)
        # 4th step create soup object to parse content
        soup = BeautifulSoup(src, 'html.parser')
        page_limit = int(soup.find('strong').text)
        if (page_num > page_limit // 15):
            print('pages ended')
            break
        # print(soup)
        # 5th step find all elements that contain info we need
        # jop_titles,company_names, job_skills, location_names,job_date,job_skills,
        job_titles = soup.find_all('h2', {'class': 'css-m604qf'})
        # print(job_titles)
        company_names = soup.find_all('a', {'class': 'css-17s97q8'})
        # print(company_names)
        job_skills = soup.find_all('div', {'class': 'css-y4udm8'})
        # print(job_skills)
        location_names = soup.find_all('span', {'class': 'css-5wys0k'})
        # print(location_names)
        posted_new = soup.find_all('div', {'class': 'css-4c4ojb'})
        posted_old = soup.find_all('div', {'class': 'css-do6t5g'})
        posted = [*posted_new, *posted_old]
        # 6th step loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            job_skill.append(job_skills[i].text)
            location_name.append(location_names[i].text)
            date.append(posted[i].text)
        page_num += 1
    except:
        print('Error occurred')
        break
for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    salaries = soup.find_all('span', {'class': 'css-4xky9y'})
    salary.append(salaries.text.strip())  # type: ignore
    requirements = soup.find('div', {'class': 'css-1t5f0fr'}).ul  # type:ignore
    respon_text = ""
    for li in requirements.find_all('li'):
        respon_text += li.text+"| "
    respon_text = respon_text[:-2]
    responsibilities.append(respon_text)
# print(salary)
# print(job_title)
# print(company_name)
# print(job_skill)
# print(location_name)
# 7th create csv file and fill it with with values
file_list = ([job_title, company_name, date, location_name,
             job_skill, links, salary, responsibilities])
exported = zip_longest(*file_list)
with open('F:/Programing/python/Web Scrapping/jobs.csv', 'w') as f:
    wr = csv.writer(f)
    wr.writerow(['job_title', 'company_name', 'date', 'location_name',
                'job_skill', 'links', 'salary', 'responsibilities'])
    wr.writerows(exported)
