from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signupTeacher, name="signup"),
    path('signin/', views.signinTeacher, name="signin"),
    path('', views.dashboard, name="dashboard"),
    path('logout/', views.logoutTeacher, name="logout")
]
