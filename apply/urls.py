from django.urls import path
from .import views

urlpatterns = [
    path('apply/<int:job_id>',views.apply_for_job,name='apply'),
    path('applied-jobs/', views.my_applied_jobs, name='applied_jobs'),
    path('job/<int:job_id>/applicants/', views.applicants_list, name='applicants_list'),
    path('job/<int:job_id>/applicant_details/', views.applicant_details, name='applicant_details'),
]