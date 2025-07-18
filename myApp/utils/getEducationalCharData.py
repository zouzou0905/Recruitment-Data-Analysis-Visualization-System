# import json
#
# from .getPublicData import *
# from myApp.models import Jobinfo
#
#
# def getPageData():
#     return list(educations.keys())
#
#
# def getAverged(list):
#     result = 0
#     for i in list:
#         result += i
#     return round(result / len(list), 2)
#
#
# def getExperienceData(educational):
#     hasEmpty = False
#     if educational == "学历不限":
#         jobs = JobInfo.objects.all()
#     else:
#         jobs = JobInfo.objects.filter(educational=educational)
#     workExperiences = {}
#     workPeople = {}
#     for i in workExperience1:
#         workExperiences[i] = []
#         workPeople[i] = 0
#     for job in jobs:
#         for k, v in workExperiences.items():
#             if job.workExperience == k:
#                 if job.practice == 0:
#                     workExperiences[k].append(json.loads(job.salary)[1])
#                     workPeople[k] += 1
#     for k, v in workExperiences.items():
#         try:
#             workExperiences[k] = getAverged(v)
#         except:
#             workExperiences[k] = 0
#
#     if len(jobs) == 0:
#         hasEmpty = True
#     return workExperience1, list(workExperiences.values()),list(workPeople.values()),hasEmpty
#
# def getPeopleData():
#     jobs = getAllJobs()
#     educationData = {}
#     for i in jobs:
#         if educationData.get(i.educational,-1) == -1:
#             educationData[i.educational] = 1
#         else:
#             educationData[i.educational] += 1
#     return list(educationData.keys()), list(educationData.values())


from .getPublicData import *
from myApp.models import Jobinfo
import json

def getPageData():
    return list(educations.keys())

import json

def getAverged(salary_list):
    if not salary_list:  # 检查列表是否为空
        return 0
    result = sum(salary_list)
    return round(result / len(salary_list), 2)

def getExperienceData(educational):
    hasEmpty = False
    if educational == "学历不限":
        jobs = Jobinfo.objects.all()
    else:
        jobs = Jobinfo.objects.filter(educational=educational)
    workExperiences = {}
    workPeople = {}
    for i in workExperience1:  # 假设 workExperience1 是一个包含不同工作年限的列表
        workExperiences[i] = []
        workPeople[i] = 0
    for job in jobs:
        if job.practice == 0:  # 如果是实习岗位，则跳过当前循环
            continue
        salary_data = None
        try:
            salary_data = json.loads(job.salary)
            if isinstance(salary_data, list) and len(salary_data) >= 2:
                salary = salary_data[1]  # 假设我们想要的是薪资范围的上限
            else:
                raise ValueError("Invalid salary format.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing salary for job ID {job.id}: {e}")
            continue  # 跳过当前循环，处理下一个 job
        for k, v in workExperiences.items():
            if job.workExperience == k:
                workExperiences[k].append(salary)
                workPeople[k] += 1
    for k, v in workExperiences.items():
        workExperiences[k] = getAverged(v) if v else 0

    if len(jobs) == 0 or all(value == 0 for value in workPeople.values()):
        hasEmpty = True
    return workExperience1, list(workExperiences.values()), list(workPeople.values()), hasEmpty

def getPeopleData():
    jobs = getAllJobs()
    educationData = {}
    for i in jobs:
        if educationData.get(i.educational,-1) == -1:
            educationData[i.educational] = 1
        else:
            educationData[i.educational] += 1
    return list(educationData.keys()), list(educationData.values())
