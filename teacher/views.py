from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from datetime import datetime

from .models import *
from .forms import TeacherSignUpForm, TeacherSignInForm, AttendanceForm
from .decorators import verify

@verify
def signupTeacher(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            password = form.cleaned_data['password']
            teacher.set_password(password)
            teacher.save()
            messages.success(request, 'Account successfully created.')
            return redirect('teacher:signin')
        else:
            messages.error(request, 'Email or Username already taken.')
    
    form = TeacherSignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'teacher/signup.html', context)

@verify
def signinTeacher(request):
    if request.method == 'POST':
        form = TeacherSignInForm(request.POST)        
        email = form['email'].value()
        password = form['password'].value()
        user = authenticate(request, username = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('teacher:dashboard')
        else:
            messages.error(request, 'Incorrect email or password.')
        
    form = TeacherSignInForm()
    context = {
        'form': form
    }
    return render(request, 'teacher/signin.html', context)

def signoutTeacher(request):
    logout(request)
    return redirect('teacher:signin')

@login_required(login_url='teacher:signin')
def dashboard(request):
    assigned_course = Course.objects.filter(teacher = request.user).values()
    
    context = {
        'courses': assigned_course,
        'nav': 'dashboard'
    }
    return render(request, 'teacher/dashboard.html', context)


@login_required(login_url='teacher:signin')
def takeattendance(request, code):
    course = Course.objects.filter(code=code).values()
    students = Student.objects.filter(semester = course[0]['semester_id']).order_by('roll_no').values()
    no_of_students = 0
    attendance_info = []
    for student in students:
        info = {
            'student_name': student['first_name'] + ' ' +  student['last_name'],
            'course_id': course,
            'student_id': student['registration_no'],
            'roll_no': student['roll_no']
        }
        attendance_info.append(info)
        no_of_students += 1

    forms = formset_factory(AttendanceForm, max_num=no_of_students)
    forms = forms(initial=attendance_info)
    
    context = {
        'forms': forms,
        'date': datetime.today().strftime('%Y-%m-%d'),
        'course_title': course[0]['title'], 
    }
    return render(request, 'teacher/takeattendance.html', context)

@login_required(login_url='teacher:signin')
def redtakeattendance(request):
    return redirect('teacher:dashboard')

@login_required(login_url='teacher:signin')
def history(request):
    return render(request, 'teacher/history.html', {'nav': 'history'})
