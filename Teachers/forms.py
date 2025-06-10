from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta :
        model = Problem
        fields = ['title', 'description', 'input_description' , 'output_description' ,'example', 'sample_input', 'expected_output']