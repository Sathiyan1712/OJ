from django.urls import path
from . import views

urlpatterns=[
    path("",views.home, name='home'),
    path("chose-action",views.choose_action, name='chose it'),
    path("register", views.Register, name='regis'),
    # path("register-student", views.Register_stud, name='regis-stud'),
    # path("login-teacher", views.Login_teach, name='login-teach'),
    path("login", views.Login, name='login'),
    path('logout', views.logout_view, name='logout'),
]