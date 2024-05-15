from django.shortcuts import render, redirect
from .forms import ApplyForm
from job.models import JobDetails

def apply_for_job(request, id):
    job = JobDetails.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicants = request.user
            application.job = job
            application.save()
            return redirect('job_details', id=id)
    else:
        form = ApplyForm()
    
    return render(request, 'apply_form.html', {'form': form, 'job': job})
