from django.shortcuts import render
from .forms import TeacherSignUpForm
from django.contrib import messages


def signupTeacher(request):
    form = TeacherSignUpForm()
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
            form = TeacherSignUpForm()
            messages.success(request, 'Account successfully created.')
        else:
            form = TeacherSignUpForm()
            messages.error(request, 'Email or Username already taken.')
    context = {
        'form': form,
    }
    return render(request, 'teacher/signup.html', context)

def signinTeacher(request):
    form = TeacherSignUpForm()
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
    else: 
        form = TeacherSignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'teacher/signin.html', context)