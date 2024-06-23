from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ApplyForm
from job.models import JobDetails
from django.http import HttpResponse
from .models import Apply
from django.contrib import messages

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobDetails, pk=job_id)
    if job.user == request.user:
        return HttpResponse("You cannot apply for your own posted job.", status=403)
    
    if request.method == 'POST':
        form = ApplyForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicants = request.user
            application.job = job
            application.save()
            
            job.applicants += 1
            job.save()

            return redirect('job_details', job_id=job_id)
    else:
        form = ApplyForm()
    
    return render(request, 'apply_form.html', {'form': form, 'job': job})

@login_required
def my_applied_jobs(request):
    applied_jobs = Apply.objects.filter(applicants=request.user)
    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})

@login_required
def applicants_list(request, job_id):
    job = get_object_or_404(JobDetails, pk=job_id)
    applicants = Apply.objects.filter(job=job)
    return render(request, 'applicants_list.html', {'job': job, 'applicants': applicants})

@login_required
def applicant_details(request, apply_id):
    applicant = get_object_or_404(Apply, pk=apply_id)
    return render(request, 'applicant_details.html', {'applicant': applicant})

@login_required
def delete_applicant(request, apply_id):
    applicant = get_object_or_404(Apply, pk=apply_id)
    if request.method == 'POST':
        applicant.delete()
        messages.success(request, 'Applicant has been deleted successfully.')
        return redirect('applied_jobs')
    return redirect('applied_jobs')