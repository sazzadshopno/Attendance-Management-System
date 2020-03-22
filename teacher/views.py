from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
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
    message = None
    if 'error_message' in request.session:
        message = request.session['error_message']
        del request.session['error_message']
        messages.error(request, message)

    context = {
        'courses': assigned_course,
        'nav': 'dashboard'
    }
    return render(request, 'teacher/dashboard.html', context)


@login_required(login_url='teacher:signin')
def takeattendance(request, code):
    today = datetime.today().strftime('%Y-%m-%d')
    course = Course.objects.filter(code=code).values()
    get_attendance = Attendance.objects.filter(date=today).filter(course_id=code).count()
    if get_attendance > 0:
        request.session['error_message'] = ('Attendance of %s for %s already taken.') % (course[0]['title'], today)
        return redirect('teacher:dashboard')
    students = Student.objects.filter(semester = course[0]['semester_id']).order_by('roll_no').values()
    no_of_students = 0
    attendance_info = []
    for student in students:
        info = {
            'student_name': student['first_name'] + ' ' +  student['last_name'],
            'course_id': course[0]['code'],
            'student_id': student['registration_no'],
            'roll_no': student['roll_no'],
            'status': False,
            'date': today
        }
        attendance_info.append(info)
        no_of_students += 1

    formset = formset_factory(AttendanceForm, max_num=no_of_students)
    if request.method == 'POST':
        forms = formset(request.POST)
        if forms.is_valid():
            for form in forms:
                if form.is_valid():
                    course_id = Course.objects.get(code = form.cleaned_data['course_id'])
                    student_id = Student.objects.get(registration_no = form.cleaned_data['student_id'])
                    date = form.cleaned_data['date']
                    status = form.cleaned_data['status']
                    attendance_model = Attendance.objects.create(
                        course = course_id,
                        student = student_id,
                        date = date,
                        status = status
                    )
                    attendance_model.save()
            return redirect('teacher:dashboard')
        else:
            return HttpResponseNotFound('Not working')

    forms = formset(initial=attendance_info)
    
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
