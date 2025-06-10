from django.urls import path
from . import views

urlpatterns=[
    path('teacher-dashboard', views.teacher_home, name = 'teach_dashboard'),   
    path('teacher-problems', views.problems, name = 'problems'),    
    path('teacher-add-problem', views.add_problem, name = 'add_problem'),
    path('teacher-remove-problem', views.remove_problem, name = 'remove_problem'),
    path('<int:pk>', views.problem_detail, name= 'problem_detail'),
    path('Tproblem/<int:pk>/submissions/', views.Tproblem_submissions, name='Tproblem_submissions'),
    path('Tsubmission/<int:submission_id>/', views.Tview_code_submission, name='Tview_code_submission'),
    
    # path('teacher-dashboarsdgd', views.remove_problem, name = 'logout'),
    


]