from django.shortcuts import render, redirect,get_object_or_404, redirect
from .models import Skill,JobDetails
from .import forms
from django.contrib.auth.decorators import login_required
from .forms import EditJobForm

def SkillView(request):
    if request.method == 'POST': 
        Skill_form = forms.SkillForm(request.POST)
        if Skill_form.is_valid():
            Skill_form.save()
            return redirect('skill')
    else:
        Skill_form = forms.SkillForm()
    return render(request, 'skills.html',{'form':Skill_form})

def create_or_edit_job(request, job_id=None):
    if job_id:
        job = JobDetails.objects.get(pk=job_id)
        form = forms.JobDetailsForm(request.POST or None, instance=job)
    else:
        job = None
        form = forms.JobDetailsForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user 
            job.save()
            return redirect('home') 

    return render(request, 'job_post.html', {'form': form, 'job': job})

def job_detail(request, job_id):
    job = JobDetails.objects.get(pk=job_id)
    return render(request, 'job_details.html', {'job': job})

@login_required
def user_job_posts(request):
    jobs = JobDetails.objects.filter(user=request.user)
    return render(request, 'posted_job.html', {'jobs': jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobDetails, pk=job_id)
    
    if request.method == 'POST':
        form = EditJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_details', job_id=job_id)
    else:
        form = EditJobForm(instance=job)
    
    return render(request, 'edit_jobs.html', {'form': form, 'job': job})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobDetails, pk=job_id, user=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('posted_job')
    return redirect('posted_job')