from django import forms
from submit.models import CodeSubmit


LANGUAGECHOICE= [
    ('cpp','C++'),
    
    
]

class submitform (forms.ModelForm):
    language = forms.ChoiceField(choices= LANGUAGECHOICE)

    class Meta:
        model = CodeSubmit
        fields = ["language", "code", "input"]