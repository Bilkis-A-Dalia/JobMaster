from django.db import models
from django.contrib.auth.models import User
from job.models import JobDetails
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Apply(models.Model):
    applicants = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDetails, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='apply/media/uploads/', validators=[validate_file_extension])
    cover_letter = models.TextField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.applicants} - {self.job.title}"
