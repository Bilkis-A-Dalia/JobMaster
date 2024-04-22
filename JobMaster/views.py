from django.shortcuts import render
from job.models import JobDetails
from category.models import Category, JobType

def Home(request, category_slug=None, job_type_slug=None):
    jobs = JobDetails.objects.all()

    # Filter jobs by category if category_slug is provided
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        jobs = jobs.filter(category=category)

    # Filter jobs by job type if job_type_slug is provided
    if job_type_slug is not None:
        job_type = JobType.objects.get(slug=job_type_slug)
        jobs = jobs.filter(work_type=job_type)

    categories = Category.objects.all()
    job_types = JobType.objects.all()

    return render(request, 'home.html', {'jobs': jobs, 'categories': categories, 'job_types': job_types})
