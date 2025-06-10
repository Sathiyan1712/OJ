from django.db import models
from django.conf import settings # Import settings to reference AUTH_USER_MODEL
from Teachers.models import Problem

# Create your models here.
class CodeSubmit(models.Model):
    
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='code_submissions')

    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True, related_name='submissions')

    language= models.CharField(max_length=50)
    code = models.TextField()
    input = models.TextField(null=True, blank =True)
    output = models.TextField(null = True, blank= True)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)