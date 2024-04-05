from  .import views
from django.urls import path
 
urlpatterns = [
    path('job_post/',views.create_or_edit_job,name = 'create_job'),
    path('job_details/',views.job_detail,name = 'job_details'),
    path('skills/',views.SkillView,name = 'skill'),  
]
