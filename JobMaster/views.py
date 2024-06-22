from django.shortcuts import render,redirect
from job.models import JobDetails
from category.models import Category, JobType
from user.forms import ReviewForm
from user.models import Review

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

    # Handle search query
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(job_about__icontains=query)

    categories = Category.objects.all()
    job_types = JobType.objects.all()

    review = Review.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.email = request.user.email
            review.save()
            return redirect('home')  # Adjust this redirect as needed
    else:
        form = ReviewForm()

    return render(request, 'home.html', {
        'jobs': jobs,
        'categories': categories,
        'job_types': job_types,
        'search_query': query,
        'form': form,
        'review': review,
    })