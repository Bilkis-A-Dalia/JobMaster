from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ApplyForm
from job.models import JobDetails

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobDetails, pk=job_id)
    
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicants = request.user
            application.job = job
            application.save()
            return redirect('job_details', job_id=job_id)
    else:
        form = ApplyForm()
    
    return render(request, 'apply_form.html', {'form': form, 'job': job})
