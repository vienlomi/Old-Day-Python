import time
import requests
from bs4 import BeautifulSoup as bs 
import mysql.connector
import datetime
import random
import requests
from bs4 import BeautifulSoup as bs

e = 0
url = ['https://www.topcv.vn/tim-viec-lam-data-tai-ha-noi-kl1?salary=0&exp=0&company_field=0&page=']
def add_job(title, company, link):
    job = mysql.connector.connect(option_files="D:\Python\Mysql\my.ini")
    cursor = job.cursor()
    insert_query = """insert into job.jobs (title, company, link, date) values (\'{title}\',\'{company}\', \'{link}\', \'{date}\')
    """.format(title=title, company=company, link=link, date=str(datetime.datetime.today()))
    print(insert_query)
    try:
        cursor.execute(insert_query)
    except:
        e += 1
    job.commit()
    cursor.close()
    job.close()

def get_job_topcv(url):
    topcv = requests.get(url)
    time.sleep(1+ random.random())
    all_job = bs(topcv.text, 'html.parser')
    title = all_job.find_all('h4', class_ = 'job-title')
    titles = [i.text.strip() for i in title]
    company = [i.parent.find('div', class_ = 'row-company').text.strip() for i in title]
    link = [i.find('a')['href'] for i in title]
    return titles, company, link


for i in range(2,6):
    job, title, link = get_job_topcv(url[0]+str(i))
    for i in zip(job, title, link):
        add_job(i[0], i[1], i[2])

print('Errors: ', e)