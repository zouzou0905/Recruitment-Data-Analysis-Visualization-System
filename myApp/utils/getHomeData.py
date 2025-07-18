from .getPublicData import *
import time
import json
from datetime import datetime


def getNowTime():
    timeFormat = time.localtime()
    yer = timeFormat.tm_year
    mon = timeFormat.tm_mon
    day = timeFormat.tm_mday
    return yer, monthList[mon - 1], day


def getUserCreateTime():
    users = getAllUsers()
    data = {}
    for u in users:
        if isinstance(u.createTime, datetime):
            create_time_str = u.createTime.strftime('%Y-%m-%d')
        else:
            create_time_str = str(u.createTime)
        if data.get(create_time_str, -1) == -1:
            data[create_time_str] = 1
        else:
            data[create_time_str] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name': k,
            'value': v
        })
    return result


def getUserTop6():
    users = getAllUsers()
    def sort_fn(user):
        try:
            return time.mktime(time.strptime(str(user.createTime), '%Y-%m-%d'))
        except ValueError:
            return time.mktime(time.localtime())
    users = sorted(users, key=sort_fn, reverse=True)[:6]
    return users


def getAllTags():
    jobs = Jobinfo.objects.all()
    users = User.objects.all()
    educationsTop = '学历不限'
    salaryTop = 0
    salaryMonthTop = 0
    dist = {}  # 存储城市频率
    practice = {}

    # 从 address 提取城市名
    def get_city(address):
        """从 address 字段提取城市名（如 '北京海淀区' → '北京'）"""
        # 匹配直辖市和常见城市前缀
        for city in ['北京', '上海', '天津', '重庆', '广州', '深圳', '杭州', '成都', '长沙', '苏州', '南京', '西安', '合肥', '厦门']:
            if address.startswith(city):
                return city
        # 其他情况：提取第一个市级名称（如 '郑州市金水区' → '郑州'）
        if '市' in address:
            return address.split('市')[0] + '市'
        return address  # 保底返回原值

    for job in jobs:

        if job.educational in educations and educations[job.educational] < educations[educationsTop]:
            educationsTop = job.educational

        try:
            salary = json.loads(job.salary)[1]
            if salaryTop < salary:
                salaryTop = salary
        except (json.JSONDecodeError, IndexError):
            continue

        if int(job.salaryMonth) > salaryMonthTop:
            salaryMonthTop = int(job.salaryMonth)

        city = get_city(job.address)  # 关键改动！
        dist[city] = dist.get(city, 0) + 1

        if practice.get(job.practice, -1) == -1:
            practice[job.practice] = 1
        else:
            practice[job.practice] += 1

    distStr = sorted(dist.items(), key=lambda x: x[1], reverse=True)[:3]
    distTop = ''
    for index, item in enumerate(distStr):
        if index == len(distStr) - 1:
            distTop += item[0]
        else:
            distTop += item[0] + '.'
    practiceMax = sorted(practice.items(), key=lambda x: x[1], reverse=True)
    return len(jobs), len(users), educationsTop, salaryTop, distTop, salaryMonthTop, practiceMax[0][0]


def getAllJobsPBar():
    jobs = getAllJobs()
    tempData = {}
    for job in jobs:
        createTime = str(job.createTime)[:10]
        if tempData.get(createTime, -1) == -1:
            tempData[createTime] = 1
        else:
            tempData[createTime] += 1
    def sort_fn(item):
        dt = time.strptime(item[0], '%Y-%m-%d')
        return time.mktime(dt)
    result = sorted(tempData.items(), key=sort_fn)
    def map_fn(item):
        dt = time.strptime(item[0], '%Y-%m-%d')
        formatted_date = time.strftime('%Y-%m-%d', dt)
        item = [formatted_date, item[1]]
        item.append(round(item[1] / len(jobs), 3))
        return item
    result = list(map(map_fn, result))
    return result


def getTablaData():
    jobs = getAllJobs()
    for i in jobs:
        try:
            company_tags = json.loads(i.companyTags)
            if isinstance(company_tags, list) and company_tags != ["无"]:
                i.companyTags = ','.join(map(str, company_tags))
            else:
                i.companyTags = '无'
        except json.JSONDecodeError:
            i.companyTags = '未知'
        try:
            work_tag_str = i.workTag.replace("'", '"')
            work_tag = json.loads(work_tag_str)
            if isinstance(work_tag, list) and work_tag != ["无"]:
                i.workTag = ','.join(map(str, work_tag))
            else:
                i.workTag = '无'
        except json.JSONDecodeError:
            i.workTag = '未知'
        if i.companyPeople == "[0,10000]":
            i.companyPeople = "10000人以上"
        else:
            try:
                i.companyPeople = json.loads(i.companyPeople)
                if isinstance(i.companyPeople, list):
                    i.companyPeople = '-'.join([str(x) + '人' for x in i.companyPeople])
                else:
                    i.companyPeople = '未知'
            except json.JSONDecodeError:
                i.companyPeople = '未知'
        try:
            i.salary = json.loads(i.salary)[1]
        except (json.JSONDecodeError, IndexError):
            i.salary = '未知'
    return jobs