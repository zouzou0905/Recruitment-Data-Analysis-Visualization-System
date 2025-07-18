from .getPublicData import *
import json
import re
def getPageData():
    jobs = getAllJobs()
    typeData = []
    for i in jobs: typeData.append(i.type)
    return list(set(typeData))

def getCompanyBar(type):
    if type == 'all':
        jobs = Jobinfo.objects.all()
    else:
        jobs = Jobinfo.objects.filter(type=type)
    natureData = {}
    for i in jobs:
        if natureData.get(i.companyNature, -1) == -1:
            natureData[i.companyNature] = 1
        else:
            natureData[i.companyNature] += 1
    natureList = list(sorted(natureData.items(), key=lambda x: x[1], reverse=True))
    rowData = []
    columnData = []
    for k, v in natureList:
        rowData.append(k)
        columnData.append(v)
    return rowData[:20], columnData[:20]


# def getCompanyPie(type):
#     if type == 'all':
#         jobs = Jobinfo.objects.all()
#     else:
#         jobs = JobIinfo.objects.filter(type=type)
#     addressData = {}
#     for i in jobs:
#         if addressData.get(i.address, -1) == -1:
#             addressData[i.address] = 1
#         else:
#             addressData[i.address] += 1
#     result = []
#     for k, v in addressData.items():
#         result.append({
#             'name': k,
#             'value': v
#         })
#     return result




def getCompanyPie(type):
    jobs = Jobinfo.objects.all() if type == 'all' else Jobinfo.objects.filter(type=type)
    city_data = {}

    for job in jobs:
        full_address = job.address
        # 使用正则匹配：提取连续的中文字符（直到遇到非中文或分隔符）
        match = re.match(r'^[\u4e00-\u9fa5]+', full_address)
        city = match.group() if match else full_address
        city = city.strip()
        city_data[city] = city_data.get(city, 0) + 1

    result = [{'name': k, 'value': v} for k, v in city_data.items()]
    return result[:25]


# def getCompanyPie(type):
#     # 查询数据库（确保模型名称正确）
#     if type == 'all':
#         jobs = Jobinfo.objects.all()
#     else:
#         jobs = Jobinfo.objects.filter(type=type)
#
#     city_data = {}
#
#     for job in jobs:
#         full_address = job.address
#         # 分割地址提取城市（兼容无"."的情况）
#         if '.' in full_address:
#             city = full_address.split('.')[0].strip()
#         else:
#             city = full_address.strip()
#
#         city_data[city] = city_data.get(city, 0) + 1
#
#     # 按城市出现次数降序排序，并取前20条
#     sorted_cities = sorted(
#         city_data.items(),
#         key=lambda x: x[1],  # 按出现次数排序
#         reverse=True  # 降序（从高到低）
#     )[:20]  # 截取前20项
#
#     # 生成结果格式
#     result = [{'name': city, 'value': count} for city, count in sorted_cities]
#     return result[:30]


def getCompanyPeople(type):
    if type == 'all':
        jobs = Jobinfo.objects.all()
    else:
        jobs = Jobinfo.objects.filter(type=type)
    def map_fn(item):
        item.companyPeople = json.loads(item.companyPeople)[1]
        return item
    jobs = list(map(map_fn, jobs))
    data = [0 for x in range(6)]
    for i in jobs:
        p = i.companyPeople
        if p <= 20:
            data[0] += 1
        elif p <= 100:
            data[1] += 1
        elif p <= 500:
            data[2] += 1
        elif p <= 1000:
            data[3] += 1
        elif p < 10000:
            data[4] += 1
        else:
            data[5] += 1
    return companyPeople,data