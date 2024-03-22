from django import forms 
from . models import Category,JobType

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'