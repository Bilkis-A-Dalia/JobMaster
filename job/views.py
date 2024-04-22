from django.shortcuts import render, redirect
from .models import Skill,JobDetails
from .import forms

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