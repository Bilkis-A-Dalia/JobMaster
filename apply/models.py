from django.db import models
from django.contrib.auth.models import User
from job.models import JobDetails
# Create your models here.

class Apply(models.Model):
    applicants = models.ForeignKey(User,on_delete = models.CASCADE)
    job = models.ForeignKey(JobDetails, on_delete = models.CASCADE)
    resume = models.FileField(upload_to = 'apply/media/uploads/')
    cover_letter = models.TextField()
    availability = models.BooleanField(default=True)
    def __str__(self):
        return self.applicants,self.job.title