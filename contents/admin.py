from django.contrib import admin
from .models import (
                     EmailContents,
                     ProfessorDev,
                     StartUp,
                     FinanceReport,
                     Tag,
                     Rescue,
                     RescueUpdateCheck
                     )
# Register your models here.

class EmailContentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'registered_dttm')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProfessorDevAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'category')


class StartUpAdmin(admin.ModelAdmin):
    list_display = ('name', 'invest_stage', 'category')


class FinanceReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'security_firm', 'category')


class RescueAdmin(admin.ModelAdmin):
    list_display = ('date', 'area', 'company_name', 'case_num', 'subject')


class RescueUpdateCheckAdmin(admin.ModelAdmin):
    list_display = ('recent_date',)

admin.site.register(EmailContents, EmailContentsAdmin)
admin.site.register(ProfessorDev, ProfessorDevAdmin)
admin.site.register(StartUp, StartUpAdmin)
admin.site.register(FinanceReport, FinanceReportAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Rescue, RescueAdmin)
admin.site.register(RescueUpdateCheck, RescueUpdateCheckAdmin)