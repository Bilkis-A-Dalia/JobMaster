from django.contrib import admin
from .import models
# Register your models here.

class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','slug']

class JobTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('type',)}
    list_display = ['type','slug']

admin.site.register(models.Category, categoryAdmin)
admin.site.register(models.JobType, JobTypeAdmin)