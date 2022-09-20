from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from datetime import datetime

from .models import *
from .forms import AttendanceDateForm, TeacherSignUpForm, TeacherSignInForm, AttendanceForm
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
    today = datetime.today().strftime('%Y-%m-%d')
    assigned_course = Course.objects.filter(teacher = request.user).values()
    message = None
    if 'error_message' in request.session:
        message = request.session['error_message']
        del request.session['error_message']
        messages.error(request, message)

    context = {
        'courses': assigned_course,
        'nav': 'dashboard',
        'attendance_date': today
    }
    return render(request, 'teacher/dashboard.html', context)


@login_required(login_url='teacher:signin')
def takeattendance(request, code):
    today = request.GET.get('attendance_date', datetime.today().strftime('%Y-%m-%d'))
    # # today = datetime.today().strftime('%Y-%m-%d')
    # print(request.GET)
    course = Course.objects.filter(code=code).values()
    
    students = Student.objects.filter(semester = course[0]['semester_id']).order_by('roll_no').values()
    no_of_students = 0
    attendance_info = []

    for student in students:
        current_student_status = Attendance.objects.filter(date=today, course_id=code, student_id=student['registration_no']).order_by('-createdAt').first()
        info = {
            'student_name': student['first_name'] + ' ' +  student['last_name'],
            'course_id': course[0]['code'],
            'student_id': student['registration_no'],
            'roll_no': student['roll_no'],
            'status': current_student_status.status if current_student_status else False,
            'date': today
        }
        attendance_info.append(info)
        no_of_students += 1

    formset = formset_factory(AttendanceForm, max_num=no_of_students)
    if request.method == 'POST':
        forms = formset(request.POST)
        if forms.is_valid():
            total_student = 0
            total_present = 0
            total_absent = 0
            for form in forms:
                if form.is_valid():
                    course_id = Course.objects.get(code = form.cleaned_data['course_id'])
                    student_id = Student.objects.get(registration_no = form.cleaned_data['student_id'])
                    date = form.cleaned_data['date']
                    status = form.cleaned_data['status']
                    total_student += 1
                    
                    if status:
                        total_present += 1
                    else:
                        total_absent += 1

                    current_student_status = Attendance.objects.filter(date=today, course_id=code, student_id=student_id).order_by('-createdAt').first()
                    
                    if current_student_status:
                        attendance_model = Attendance.objects.filter(date=today, course_id=code, student_id=student_id).update(
                            course = course_id,
                            student = student_id,
                            date = date,
                            status = status
                        )
                    else: 
                        attendance_model = Attendance.objects.create(
                            course = course_id,
                            student = student_id,
                            date = date,
                            status = status
                        )
                        attendance_model.save()
            absent_percentage = ((total_student-total_present)/total_student) * 100
            present_percentage = 100 - absent_percentage
            context = {
                'total_student': total_student,
                'total_present': total_present,
                'total_absent': total_absent,
                'absent_percentage': absent_percentage,
                'present_percentage': present_percentage
            }
            return render(request, 'teacher/report.html', context)
        else:
            return HttpResponseNotFound('Error while submiting the attendance. Please try again later.')

    forms = formset(initial=attendance_info)
    
    context = {
        'forms': forms,
        'date_form': AttendanceDateForm(),
        'date': datetime.today().strftime('%Y-%m-%d'),
        'course_title': course[0]['title'], 
    }

    return render(request, 'teacher/takeattendance.html', context)


@login_required(login_url='teacher:signin')
def redtakeattendance(request):
    return redirect('teacher:dashboard')

@login_required(login_url='teacher:signin')
def history(request):
    courses = Course.objects.filter(teacher = request.user).values()
    return render(request, 'teacher/history.html', {'nav': 'history', 'courses': courses})
    
@login_required(login_url='teacher:signin')
def viewhistory(request, code):
    # Dates of attendances taken
    dates = Attendance.objects.filter(course_id=code).order_by('-date').values('date').distinct()
    # Get the details of the course using code
    course = Course.objects.filter(code=code).values()
    # Get the student list who enrolled this course
    students = Student.objects.filter(semester = course[0]['semester_id']).order_by('roll_no').values()
    student_info = []
    for student in students:
        std = {
            'name': student['first_name'] + ' ' +  student['last_name'],
            'roll_no': student['roll_no']
        }
        attendances = []
        for date in dates:
            atndance = Attendance.objects.filter(course_id = code).filter(date = date['date']).filter(student_id=student['registration_no']).values()
            attendances.append('P' if atndance[0]['status'] == True else 'A')
        std.update(
            {'attendances': attendances}
        )
        student_info.append(std)
    context = {
        'student_info': student_info,
        'dates': dates,
        'course': course[0]['title']
    }
    return render(request, 'teacher/details.html', context)