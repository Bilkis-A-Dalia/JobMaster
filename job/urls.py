from django.urls import path
from . import views

urlpatterns = [
    path('job_post/', views.create_or_edit_job, name='create_job'),
    path('job_details/<int:job_id>/', views.job_detail, name='job_details'),
    path('skills/', views.SkillView, name='skill'),  
]
