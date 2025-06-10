from django.urls import path
from .  import views

urlpatterns =[
    path('', views.student_home, name='Stud home'),
    path('Problem-list', views.Student_Problem, name = 'Prob list'),
    path ('Problem-detail/<int:pk>', views.ProblemDetail, name = 'prob det'),
    path('problem/<int:pk>/submissions/', views.problem_submissions, name='problem_submissions'),
    path('submission/<int:submission_id>/', views.view_code_submission, name='view_code_submission'),

    # path('cCompiler/<int:pk>', views.Solve_problem, name= 'solve problem')

    
]