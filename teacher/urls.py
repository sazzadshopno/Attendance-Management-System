from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.signupTeacher, name="signup"),
    path('signin/', views.signinTeacher, name="signin"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logoutTeacher, name="logout")
]
