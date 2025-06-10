from django.urls import path
from submit import views

urlpatterns=[
    path('compiler/<int:problem_id>', views.submit, name ='code submit'),
    path('ai_review/<int:submission_id>/', views.ai_review_code, name='ai_review_code'),
    
]