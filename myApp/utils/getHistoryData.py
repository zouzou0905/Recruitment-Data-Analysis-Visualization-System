from .getPublicData import *
from myApp.models import History
from django.db.models import F
import json


def addHistory(userInfo,jobId):
    # print(userInfo,jobId)
    hisData = History.objects.filter(user=userInfo,job_id=jobId)
    if len(hisData):
        hisData[0].count = F('count') + 1
        hisData[0].save()
    else:
        History.objects.create(user=userInfo,job_id=jobId)

def getHistoryData(userInfo):
    data = list(History.objects.filter(user=userInfo).order_by('-count'))
    def map_fn(item):
        # 假设 item.job.salary 和 item.job.companyPeople 是 JSON 字符串
        item.job.salary = json.loads(item.job.salary)
        item.job.companyPeople = json.loads(item.job.companyPeople)

        # 对 workTag 进行处理
        if item.job.workTag != '无':
            cleaned_workTag = item.job.workTag.replace("'", '"')
            try:
                item.job.workTag = json.loads(cleaned_workTag)
            except json.JSONDecodeError:
                item.job.workTag = []
        else:
            item.job.workTag = []

        # 对 companyTags 进行处理
        if item.job.companyTags != '无':
            company_tags = json.loads(item.job.companyTags)
            if isinstance(company_tags, list) and len(company_tags) > 0:
                item.job.companyTags = [subtag for tag in company_tags for subtag in tag.split('，') if isinstance(tag, str)]
            else:
                item.job.companyTags = []
        else:
            item.job.companyTags = []

        # 对 salary 进行处理
        if not item.job.practice:
            item.job.salary = list(map(lambda x: str(int(x / 1000)), item.job.salary))
        else:
            item.job.salary = list(map(lambda x: str(x), item.job.salary))
        item.job.salary = '-'.join(item.job.salary)

        # 对 companyPeople 进行处理
        item.job.companyPeople = list(map(lambda x: str(x), item.job.companyPeople))
        item.job.companyPeople = '-'.join(item.job.companyPeople)

        # 对 address 进行处理
        address_parts = item.job.address.split('·')
        if len(address_parts) == 2:
            city, detail_address = address_parts
            item.job.address = f"{city}.{item.job.dist}.{detail_address}"
        else:
            item.job.address = address_parts[0] if address_parts else item.job.address

        return item

    data = list(map(map_fn,data))
    return data

def removeHistory(hisId):
    his = History.objects.get(id=hisId)
    his.delete()