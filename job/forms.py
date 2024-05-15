from django import forms
from .models import Skill,JobDetails

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        labels = {
            'name': 'Skill Name',
        }

class JobDetailsForm(forms.ModelForm):
    class Meta:
        model = JobDetails
        fields = ['title', 'company_name', 'work_type', 'category', 'starting_date', 'salary', 'experience', 'deadline', 'job_about', 'skills', 'other_req', 'vacancy']
        labels = {
            'title': 'Job Title',
            'company_name': 'Company Name',
            'work_type': 'Work Type',
            'category': 'Category',
            'starting_date': 'Starting Date',
            'salary': 'Salary',
            'experience': 'Experience',
            'deadline': 'Deadline',
            'job_about': 'Job Description',
            'skills': 'Skills Required',
            'other_req': 'Other Requirements',
            'vacancy': 'Vacancy',
        }
        widgets = {
            'starting_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'job_about': forms.Textarea(attrs={'rows': 2}),
            'other_req': forms.Textarea(attrs={'rows': 2}),
        }
