
from django.contrib import admin
from  .import views
from django.urls import path

urlpatterns = [
    path('register/',views.register,name = 'register'),
    # path('profile/',views.profile,name='profile'),
    path('profile/edit',views.edit_profile,name = 'edit_profile'),
    path('profile/resume',views.create_or_edit_resume,name = 'profile'),
    path('login/',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout,name = 'user_logout'),
    path('active/<uid64>/<token>/', views.activate,name = 'activate'),
]