import json
from .getPublicData import *

def getTableData():
    jobs = getAllJobs()

    def map_fn(item):
        item.salary = json.loads(item.salary)
        item.companyPeople = json.loads(item.companyPeople)

        if item.workTag != '无':
            cleaned_workTag = item.workTag.replace("'", '"')
            try:
                item.workTag = json.loads(cleaned_workTag)
            except json.JSONDecodeError:
                item.workTag = []
        else:
            item.workTag = []

        if item.companyTags != '无':
            company_tags = json.loads(item.companyTags)
            if isinstance(company_tags, list) and len(company_tags) > 0:
                item.companyTags = [subtag for tag in company_tags for subtag in tag.split('，') if isinstance(tag, str)]
            else:
                item.companyTags = []
        else:
            item.companyTags = []

        if not item.practice:
            item.salary = list(map(lambda x: str(int(x / 1000)), item.salary))
        else:
            item.salary = list(map(lambda x: str(x), item.salary))
        item.salary = '-'.join(item.salary)

        item.companyPeople = list(map(lambda x: str(x), item.companyPeople))
        item.companyPeople = '-'.join(item.companyPeople)

        address_parts = item.address.split('·')
        if len(address_parts) == 2:
            city, detail_address = address_parts
            item.address = f"{city}.{item.dist}.{detail_address}"
        else:
            item.address = address_parts[0] if address_parts else item.address

        return item

    jobs = list(map(map_fn, jobs))
    return jobs
