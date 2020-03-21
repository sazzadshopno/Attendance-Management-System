from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signupTeacher, name="signup"),
    path('signin/', views.signinTeacher, name="signin"),
    path('', views.dashboard, name="dashboard"),
    path('takeattendance/', views.takeattendance, name="takeattendance"),
    path('history/', views.history, name="history"),
    path('signout/', views.signoutTeacher, name="signout")
]
