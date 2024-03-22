from .import views
from django.urls import path

urlpatterns = [
    path('add/',views.add_category,name = 'add_category'),
    path('add/',views.add_jobtype,name = 'add_jobtype'),
]