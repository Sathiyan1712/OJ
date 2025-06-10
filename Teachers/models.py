from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem (models.Model):
    title = models.CharField(max_length= 255)
    description =  models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    example = models.TextField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE)

    sample_input = models.TextField(blank=True, null=True)
    expected_output = models.TextField(blank=True, null=True)

    def __str__ (self):
        return self.title
    # what this does?
class ProblemSolved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem')