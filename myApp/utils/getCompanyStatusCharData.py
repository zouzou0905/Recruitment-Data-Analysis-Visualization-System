from .getPublicData import *
from myApp.models import Jobinfo
import json

def getPageData():
    job = []
    jobs = getAllJobs()
    for i in jobs: job.append(i.type)
    return list(set(job))



def getTechnologyData(type):
    if type == '不限':
        jobs = Jobinfo.objects.all()
    else:
        jobs = Jobinfo.objects.filter(type=type)

    workTagData = {}
    for job in jobs:
        if job.workTag != '无':
            cleaned_workTag = job.workTag.replace("'", '"')
            try:
                workTag = json.loads(cleaned_workTag)
            except json.JSONDecodeError:
                workTag = []
            else:
                for w in workTag:
                    if not w:
                        break
                    workTagData[w] = workTagData.get(w, 0) + 1
        else:
            workTag = []

    result = sorted(workTagData.items(), key=lambda x: x[1], reverse=True)[:12]

    technologyRow = [k for k, v in result]
    technologyColumn = [v for k, v in result]

    return technologyRow, technologyColumn

def getCompanyStatusData():
    jobs = getAllJobs()
    statusData = {}
    for job in jobs:
        if statusData.get(job.companyStatus,-1) == -1:
            statusData[job.companyStatus] = 1
        else:
            statusData[job.companyStatus] += 1
    result = []
    for k,v in statusData.items():
        result.append({
            'name':k,
            'value':v
        })
    return result