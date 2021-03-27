from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class JobListingsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'job_id', 'job_topic', 'company_name', 'job_link', 'job_title', 'job_description',
                    'job_requirements', 'job_location', 'job_salary', 'job_qualification', 'job_type', 'job_experience')


admin.site.register(JobListings, JobListingsAdmin)
admin.site.register(CustomUser)
admin.site.register(InterviewQuestions)
admin.site.register(PracticeInterview)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(CompanyQuestion)
