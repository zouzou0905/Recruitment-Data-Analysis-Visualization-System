from .getPublicData import *
from myApp.models import Jobinfo
import json


def getPageData():
    return list(educations.keys()), workExperience1


def getBarData(defaultEducation, defaultWorkExperience):
    if defaultEducation == '学历不限' and defaultWorkExperience == '经验不限':
        jobs = Jobinfo.objects.all()
    elif defaultWorkExperience == '经验不限':
        jobs = Jobinfo.objects.filter(educational=defaultEducation)
    elif defaultEducation == '学历不限':
        jobs = Jobinfo.objects.filter(workExperience=defaultWorkExperience)
    else:
        jobs = Jobinfo.objects.filter(educational=defaultEducation, workExperience=defaultWorkExperience)

    jobType = {}
    for j in jobs:
        if j.practice == 0:
            try:
                salary_data = json.loads(j.salary)
                if isinstance(salary_data, list) and len(salary_data) > 1:
                    if jobType.get(j.type, -1) == -1:
                        jobType[j.type] = [salary_data[1]]
                    else:
                        jobType[j.type].append(salary_data[1])
            except json.JSONDecodeError:
                continue

    barData = {}
    for k, v in jobType.items():
        if not barData.get(k, 0):
            barData[k] = [0 for x in range(5)]
        for i in v:
            s = i / 1000
            if s < 10:
                barData[k][0] += 1
            elif s >= 10 and s < 20:
                barData[k][1] += 1
            elif s >= 20 and s < 30:
                barData[k][2] += 1
            elif s >= 30 and s < 40:
                barData[k][3] += 1
            else:
                barData[k][4] += 1
    legends = list(barData.keys())
    if len(legends) == 0: legends = None
    return salaryList, barData, legends


def averageFn(list):
    total = 0
    for i in list:
        total += i
    return round(total / len(list), 1)

def pieData():
    jobs = getAllJobs()
    jobsType = {}
    for j in jobs:
        if j.practice == 1:
            if jobsType.get(j.type, -1) == -1:
                jobsType[j.type] = [json.loads(j.salary)[1]]
            else:
                jobsType[j.type].append(json.loads(j.salary)[1])
    result = []
    for k, v in jobsType.items():
        result.append({
            'name': k,
            'value': averageFn(v)
        })
    return result

def getlouDouData():
    jobs = Jobinfo.objects.filter(salaryMonth__gt=0)
    data = {}
    for j in jobs:
        x = str(j.salaryMonth) + '薪'
        if data.get(x,-1) == -1:
            data[x] = 1
        else:
            data[x] += 1
    result = []
    for k, v in data.items():
        result.append({
            'name':k,
            'value':v,
        })
    return result