from django.shortcuts import render,redirect
from .import forms
# Create your views here.
def add_category(request):
    if request.method == 'POST': 
        category_form = forms.CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('add_category')
    else:
        category_form = forms.CategoryForm()
    return render(request, 'add_category.html',{'form':category_form})

def add_jobtype(request):
    if request.method == 'POST': 
        jobtype_form = forms.JobTypeForm(request.POST)
        if jobtype_form.is_valid():
            jobtype_form.save()
            return redirect('add_jobtype')
    else:
        jobtype_form = forms.JobTypeForm()
    return render(request, 'add_jobtype.html',{'form':jobtype_form})