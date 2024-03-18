from django.db import models
from category.models import Category,JobType
from django.contrib.auth.models import User
# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class JobDetails(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    company_name = models.CharField(max_length=100)
    work_type = models.ManyToManyField(JobType)
    catagory = models.ManyToManyField(Category)
    starting_date = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    experience = models.CharField(max_length=50)
    deadline = models.DateField()
    post_date = models.DateField(auto_now_add=True)
    applicants = models.IntegerField(default=0)
    job_about = models.TextField()
    skills = models.ManyToManyField(Skill)
    other_req = models.TextField()
    vacancy = models.IntegerField()

    def __str__(self):
        return self.title,self.company_name