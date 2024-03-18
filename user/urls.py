
from django.contrib import admin
from  .import views
from django.urls import path,include

urlpatterns = [
    path('register/',views.register,name = 'register'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit',views.edit_profile,name = 'edit_profile'),
    path('active/<uid64>/<token>/', views.activate,name = 'activate'),
]