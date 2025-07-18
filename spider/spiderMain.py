from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import os
import time
import json
import django
import random

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject_boss.settings')
django.setup()
from myApp.models import Jobinfo

class Spider(object):
    def __init__(self, type, page):
        self.type = type
        self.page = page
        self.spiderUrl = 'https://www.zhipin.com/web/geek/job?query=%s&city=100010000&page=%s'

    def startBrowser(self):
        service = Service('./chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(service=service, options=options)
        return browser

    def init(self):
        if not os.path.exists('./boss_10.csv'):
            with open('./boss_10.csv', 'a', newline='', encoding='utf-8-sig') as wf:
                writer = csv.writer(wf)
                writer.writerow([
                    "title", "address", "type", "educational", "workExperience", "workTag",
                    "salary", "salaryMonth", "companyTags", "hrWork", "hrName", "practice",
                    "companyTitle", "companyAvatar", "companyNature", "companyStatus",
                    "companyPeople", "detailUrl", "companyUrl", "dist"])

    def clear_csv(self):
        df = pd.read_csv('./boss_10.csv')
        df.drop_duplicates(inplace=True)
        df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))
        print("已存入MySQL数据库中，总数据为%d" % df.shape[0])
        return df.values

    def save_to_sql(self):
        data = self.clear_csv()
        for job in data:
            Jobinfo.objects.create(
                title=job[0],
                address=job[1],
                type=job[2],
                educational=job[3],
                workExperience=job[4],
                workTag=job[5],
                salary=job[6],
                salaryMonth=job[7],
                companyTags=job[8],
                hrWork=job[9],
                hrName=job[10],
                practice=job[11],
                companyTitle=job[12],
                companyAvatar=job[13],
                companyNature=job[14],
                companyStatus=job[15],
                companyPeople=job[16],
                detailUrl=job[17],
                companyUrl=job[18],
                dist=job[19])

    def save_to_csv(self, rowData):
        try:
            with open('./boss_10.csv', 'a', newline='', encoding='utf-8-sig') as wf:
                writer = csv.writer(wf)
                writer.writerow(rowData)
            #print("数据已写入 boss2.csv 文件。")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")

    def main(self, page):
        if self.page > page: return
        browser = self.startBrowser()
        print("正在爬取的页面路径:" + self.spiderUrl % (self.type, self.page))
        browser.get(self.spiderUrl % (self.type, self.page))
        time.sleep(18)
        job_list = browser.find_elements(by=By.XPATH, value='//ul[@class="job-list-box"]/li')
        for index, job in enumerate(job_list):
            try:
                 jobData = []
                 print('正在爬取第%d个数据' % (index + 1))
                 # title
                 title = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-name']").text
                 # address 改
                 addresses = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']/div[contains(@class,'job-title')]/span[@class='job-area-wrapper']/span").text.split('·')
                 address = ""
                 dist = ""
                 if len(addresses) > 0:
                    city = addresses[0]
                    if len(addresses) > 1:
                        admin_district = addresses[1]
                        dist = admin_district
                        if len(addresses) > 2:
                            address = city + "·" + "·".join(addresses[2:])
                        else:
                            address = city
                    else:
                        address = addresses[0]
                    if len(addresses) != 1:
                       dist = addresses[1]
                    else:
                       dist = ''

                 if not dist.strip():
                     continue
                 # type
                 type = self.type

                 tag_list = job.find_elements(
                         by=By.XPATH,
                         value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/ul[@class='tag-list']/li")
                 # educational
                 if len(tag_list) == 2:
                    educational = tag_list[1].text
                    workExperience = tag_list[0].text
                 else:
                    educational = tag_list[2].text
                    workExperience = tag_list[1].text
                 # hrName
                 hrName = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']").text
                 # hrWork
                 hrWork = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/div[@class='info-public']/em").text
                 # workTag 改
                 workTag_elements = job.find_elements(
                         by=By.XPATH,
                         value="./div[contains(@class,'job-card-footer')]/ul[@class='tag-list']/li")
                 def convert_unicode(text):
                     if isinstance(text, str):
                         try:
                             return text
                         except UnicodeDecodeError:
                             return text.encode('latin1').decode('unicode_escape')
                     else:
                         return text
                 workTag = list(map(convert_unicode, [x.text for x in workTag_elements]))
                 workTag_json = json.dumps(workTag, ensure_ascii=False)
                 workTag = json.loads(workTag_json)

                 # salary 改
                 salary = []
                 salaryMonth = '0薪'
                 practice = 0
                 salaries_text = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']/div[contains(@class,'job-info')]/span[@class='salary']"                ).text

                 if 'K' in salaries_text:
                     salaries_parts = salaries_text.split('·')
                     try:
                         salary_range_str = salaries_parts[0].replace('K', '').split('-')
                         salary = list(map(lambda x: int(x) * 1000, salary_range_str))
                     except ValueError:
                         salary = []
                     if len(salaries_parts) > 1:
                         salaryMonth = salaries_parts[1]

                 elif '元/月' in salaries_text:
                     try:
                         salary_range_str = salaries_text.replace('元/月', '').split('-')
                         salary = list(map(int, salary_range_str))
                     except ValueError:
                         salary = []

                 elif '元/时' in salaries_text:
                     try:
                         salary_range_str = salaries_text.replace('元/时', '').split('-')
                         hourly_salary = list(map(int, salary_range_str))
                         daily_salary = [x * 8 for x in hourly_salary]
                         monthly_salary = [x * 22 for x in daily_salary]
                         salary = monthly_salary
                         salaryMonth = '0薪'
                         practice = 1
                     except ValueError:
                         salary = []

                 elif '元/天' in salaries_text:
                     try:
                         salary_range_str = salaries_text.replace('元/天', '').split('-')
                         daily_salary = list(map(int, salary_range_str))
                         salary = [x * 22 for x in daily_salary]
                         salaryMonth = '0薪'
                         practice = 1
                     except ValueError:
                         salary = []

                # 处理包含特殊字符的薪资范围，如 '50-15薪'
                 if '薪' in salaries_text:
                     try:
                         base_salary, bonus_salary = salaries_text.split('-')
                         base_salary = base_salary.replace('薪', '').strip()
                         bonus_salary = bonus_salary.replace('薪', '').strip()
                         salary = [int(base_salary) * 1000, int(bonus_salary) * 1000]
                     except (ValueError, IndexError):
                         pass

                 # companyTitle
                 companyTitle = job.find_element(
                     by=By.XPATH ,
                     value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").text
                 # companyAvatar
                 companyAvatar = job.find_element(
                     by=By.XPATH,
                     value=".//div[@class='job-card-right']/div[@class='company-logo']/a/img").get_attribute('src')

                 companyInfos = job.find_elements(
                     by=By.XPATH,
                     value=".//div[@class='job-card-right']/div[@class='company-info']/ul[@class='company-tag-list']/li")
                 if len(companyInfos) == 3:
                     companyNature = companyInfos[0].text
                     companyStatus = companyInfos[1].text
                     companyPeoples = companyInfos[2].text
                     if companyPeoples != '10000人以上':
                         companyPeople = list(
                             map(lambda x: int(x), companyInfos[2].text.replace('人', '').split('-')))
                     else:
                         companyPeople = [0, 10000]
                 else:
                     companyNature = companyInfos[0].text
                     companyStatus = '未融资'
                     companyPeoples = companyInfos[1].text
                     if companyPeoples != '10000人以上':
                         companyPeople = list(
                             map(lambda x: int(x), companyInfos[1].text.replace('人', '').split('-')))
                     else:
                         companyPeople = [0, 10000]

                 # companyTags 改
                 companyTags = job.find_element(
                     by=By.XPATH,
                     value='./div[contains(@class,"job-card-footer")]/div[@class="info-desc"]').text
                 if not companyTags:
                     companyTags = '无'
                 else:
                     companyTags_list = []
                     for tag in companyTags.split('，'):
                         tag = tag.strip()
                         if '\\' in tag:
                             tag = tag.encode('utf-8').decode('unicode_escape')
                         companyTags_list.append(tag)
                     companyTags = json.dumps(companyTags_list, ensure_ascii=False)

                 # detailUrl
                 detailUrl = job.find_element(
                     by=By.XPATH,
                     value=".//a[@class='job-card-left']").get_attribute('href')

                 # companyUrl
                 companyUrl = job.find_element(
                     by=By.XPATH,
                     value=".//div[@class='job-card-right']/div[@class='company-info']/h3/a").get_attribute('href')

                 jobData.append(title)
                 jobData.append(address)
                 jobData.append(type)
                 jobData.append(educational)
                 jobData.append(workExperience)
                 jobData.append(workTag)
                 jobData.append(salary)
                 jobData.append(salaryMonth)
                 jobData.append(companyTags)
                 jobData.append(hrWork)
                 jobData.append(hrName)
                 jobData.append(practice)
                 jobData.append(companyTitle)
                 jobData.append(companyAvatar)
                 jobData.append(companyNature)
                 jobData.append(companyStatus)
                 jobData.append(companyPeople)
                 jobData.append(detailUrl)
                 jobData.append(companyUrl)
                 jobData.append(dist)

                 self.save_to_csv(jobData)
            except:
                 pass

        self.page += 1
        self.main(page)

if __name__ == '__main__':
    spiderObj = Spider('数据挖掘', 6)
    spiderObj.init()
    spiderObj.main(10)
    spiderObj.save_to_sql()