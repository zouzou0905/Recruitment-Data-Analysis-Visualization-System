from django.contrib import admin
from myApp.models import Jobinfo, User, History
# Register your models here.


class JobManager(admin.ModelAdmin):
    list_display = ["id", "title", "address", "type", "educational", "workExperience", "workTag", "salary",
                    "salaryMonth",
                    "companyTags"
        , "hrWork", "hrName", "practice", "companyTitle", "companyAvatar", "companyNature",
                    "companyStatus"
        , "companyPeople", "detailUrl", "companyUrl", "dist"]
    list_display_links = ["title"]
    list_editable = ['address', "address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags"
        , "hrWork", "hrName", "practice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus"
        , "companyPeople", "detailUrl", "companyUrl", "dist"]
    list_filter = ['type']
    search_fields = ['title']
    readonly_fields = ['id']
    list_per_page = 20


class UserManager(admin.ModelAdmin):
    list_display = ["id", "username", "password", "educational", "workExperience", "address", "work", "avatar"]
    list_display_links = ["username"]
    list_editable = ["password", "educational", "workExperience", "address", "work", "avatar"]
    search_fields = ['username']
    readonly_fields = ['id']
    list_per_page = 20


admin.site.register(Jobinfo, JobManager)
admin.site.register(User, UserManager)
