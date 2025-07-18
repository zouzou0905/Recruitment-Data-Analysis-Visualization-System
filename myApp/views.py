from django.shortcuts import render,redirect
from django.core.paginator import Paginator

from myApp.models import User
from .utils.error import *
import hashlib
from .utils import getHomeData
from .utils import getSelfInfo
from .utils import getChangePasswordData
from .utils import getTableData
from .utils import getHistoryData
from .utils import getSalaryCharData
from .utils import getCompanyCharData
from .utils import getEducationalCharData
from .utils import getCompanyStatusCharData




# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(pwd.encode('utf-8'))
        pwd = md5.hexdigest()
        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session['username'] = user.username
            return redirect('/myApp/home')
        except:
            return errorResponse(request, '用户名或密码出错！')
    return render(request, 'login.html')


def registry(request):
    if request.method == 'GET':
        return render(request, 'registry.html')
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        checkPwd = request.POST.get('checkPassword')
        try:
            User.objects.get(username=uname)
        except:
            if not uname : return errorResponse(request, '用户名不允许为空😡')
            if not pwd or not checkPwd : return errorResponse(request, '密码不允许为空😡')
            if pwd != checkPwd : return errorResponse(request, '两次密码不符合😡')
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            pwd = md5.hexdigest()
            User.objects.create(username=uname, password=pwd)
            return redirect('/myApp/login/')
        return errorResponse(request, '该用户名已经被注册')

def logOut(request):
    request.session.clear()
    return redirect('login')



def home(request):
    uname = request.session['username']
    userInfo = User.objects.get(username=uname)
    yer, month, day = getHomeData.getNowTime()
    userCreateData = getHomeData.getUserCreateTime()
    top6Users = getHomeData.getUserTop6()
    jobsLen, usersLen, educationsTop, salaryTop, distTop,salaryMonthTop, practiceMax = getHomeData.getAllTags()
    jobsPBarData = getHomeData.getAllJobsPBar()
    tableData = getHomeData. getTablaData()
    return render(request,'index.html',{
        'userInfo': userInfo,
        'dataInfo': {
            'year': yer,
            'month': month,
            'day': day,
        },
        'userCreateData': userCreateData,
        'top6Users': top6Users,
        'tagDic': {
            'jobsLen': jobsLen,
            'usersLen': usersLen,
            'educationsTop': educationsTop,
            'salaryTop': salaryTop,
            'distTop': distTop,
            'salaryMonthTop': salaryMonthTop,
            'practiceMax': practiceMax
        },
        'jobsPBarData': jobsPBarData,
        'tableData': tableData
    })
    # return render(request,'index.html')



def selfInfo(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    educations, workExperience1, jobList = getSelfInfo.getPageData()
    if request.method == 'POST':
        getSelfInfo.changeSelfInfo(request.POST, request.FILES)
        userInfo = User.objects.get(username=uname)
    return render(request, 'selfInfo.html', {
        'userInfo': userInfo,
        'pageData': {
        'educations': educations,
        'workExperience1': workExperience1,
        'jobList': jobList
        }
    })

def changePassword(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    if request.method == 'POST':
        res = getChangePasswordData.changePassword(userInfo, request.POST)
        if res != None:
            return errorResponse(request, res)
        userInfo = User.objects.get(username=uname)
    return render(request, 'changePassword.html', {
        'userInfo': userInfo
    })


def tableData(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    tableData = getTableData.getTableData()
    paginator = Paginator(tableData, 10)
    cur_page = 1
    if request.GET.get('page'): cur_page = int(request.GET.get('page'))

    c_page = paginator.page(cur_page)

    page_range = []
    visibleNumber = 10
    min = int(cur_page - visibleNumber / 10)
    if min < 1:
        min = 1
    max = min + visibleNumber
    if max > paginator.page_range[-1]:
        max = paginator.page_range[-1]
    for i in range(min, max):
        page_range.append(i)
    return render(request, 'tableData.html', {
        'userInfo': userInfo,
        'c_page': c_page,
        'page_range': page_range,
        'paginator': paginator
    })


def historyTableData(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    historyData = getHistoryData.getHistoryData(userInfo)
    return render(request, 'historyTableData.html', {
        'userInfo': userInfo,
        'historyData': historyData,
    })


def addHistory(request, jobId):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    getHistoryData.addHistory(userInfo, jobId)
    return redirect('historyTableData')

def removeHistory(request, hisId):
    getHistoryData.removeHistory(hisId)
    return redirect('historyTableData')



def salary(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    defaultEducation = '学历不限'
    defaultWorkExperience = '经验不限'
    if request.GET.get('educational'): defaultEducation = request.GET.get('educational')
    if request.GET.get('workExperience'): defaultWorkExperience = request.GET.get('workExperience')
    educations, workExperience1 = getSalaryCharData.getPageData()
    salaryList, barData, legends = getSalaryCharData.getBarData(defaultEducation, defaultWorkExperience)
    pieData = getSalaryCharData.pieData()
    louDouData = getSalaryCharData.getlouDouData()
    return render(request, 'salaryChar.html', {
        'userInfo': userInfo,
        'educations': educations,
        'workExperience1': workExperience1,
        'defaultEducation': defaultEducation,
        'defaultWorkExperience': defaultWorkExperience,
        'salaryList': salaryList,
        'barData': barData,
        'legends': legends,
        'pieData': pieData,
        'louDouData': louDouData,
    })



def company(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    typeList = getCompanyCharData.getPageData()
    type = 'all'
    if request.GET.get('type'): type = request.GET.get('type')
    rowBarData, columnBarData = getCompanyCharData.getCompanyBar(type)
    pieData = getCompanyCharData.getCompanyPie(type)
    companyPeople, lineData = getCompanyCharData.getCompanyPeople(type)
    return render(request, 'companyChar.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        "type": type,
        "rowBarData": rowBarData,
        "columnBarData": columnBarData,
        'pieData': pieData,
        'lineData': lineData,
        'companyPeople': companyPeople,
    })


def companyTags(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    return render(request, 'companyTags.html', {
        'userInfo': userInfo
    })


def educational(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    defaultEducation = '学历不限'
    if request.GET.get('educational'): defaultEducation = request.GET.get('educational')
    educations = getEducationalCharData.getPageData()
    workExperiences, charDataColumnOne, charDataColumnTwo, hasEmpty = getEducationalCharData.getExperienceData(
        defaultEducation)
    barDataRow, barDataColumn = getEducationalCharData.getPeopleData()
    return render(request, 'educationalChar.html', {
        'userInfo': userInfo,
        'educations': educations,
        'defaultEducation': defaultEducation,
        'workExperiences': workExperiences,
        'charDataColumnOne': charDataColumnOne,
        'charDataColumnTwo': charDataColumnTwo,
        'hasEmpty': hasEmpty,
        'barDataRow': barDataRow,
        'barDataColumn': barDataColumn,
    })



def companyStatus(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    defaultType = '不限'
    if request.GET.get('type'): defaultType = request.GET.get('type')
    typeList = getCompanyStatusCharData.getPageData()
    technologyRow, technologyColumn = getCompanyStatusCharData.getTechnologyData(defaultType)
    companyStatusData = getCompanyStatusCharData.getCompanyStatusData()
    return render(request, 'companyStatusChar.html', {
        'userInfo': userInfo,
        'typeList': typeList,
        'defaultType': defaultType,
        'technologyRow': technologyRow,
        'technologyColumn': technologyColumn,
        'companyStatusData': companyStatusData,
    })

