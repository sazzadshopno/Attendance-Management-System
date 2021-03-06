from django.urls import path, include
from . import views
app_name= "teacher"
urlpatterns = [
    path('signup/', views.signupTeacher, name="signup"),
    path('signin/', views.signinTeacher, name="signin"),
    path('', views.dashboard, name="dashboard"),

    path('takeattendance/<slug:code>', views.takeattendance, name="takeattendance"),
    path('takeattendance/', views.redtakeattendance, name="redtakeattendance"),

    path('history/', views.history, name="history"),
    path('history/<slug:code>', views.viewhistory, name="viewhistory"),
    path('signout/', views.signoutTeacher, name="signout")
]
