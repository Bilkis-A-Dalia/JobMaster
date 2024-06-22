from django.contrib import admin
from .models import Resume,Review,UserAccount
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Review)
admin.site.register(Resume)
