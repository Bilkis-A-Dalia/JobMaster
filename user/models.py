from django.db import models
from .constants import GENDER_TYPE
from django.contrib.auth.models import User

# Create your models here.
class UserAccount(models.Model):
    user=models.OneToOneField(User, related_name='account',on_delete=models.CASCADE)
    birth_date=models.DateField(null=True, blank=True)
    gender=models.CharField(max_length=10,choices=GENDER_TYPE)

    def __str__(self) -> str:
        return self.user.username
    
class Resume(models.Model):
    user = models.OneToOneField(User, related_name='resume', on_delete=models.CASCADE)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    extra_curriculum = models.TextField(blank=True, null=True)
    trainings_courses = models.TextField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resume of {self.user.username}"
    
# review model
STAR_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
    email = models.EmailField(max_length=254)
    rating = models.IntegerField(choices=STAR_CHOICES)
    text = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.reviewer.first_name} - {self.rating}'
