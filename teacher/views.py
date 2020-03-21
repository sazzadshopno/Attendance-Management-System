from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import TeacherSignUpForm, TeacherSignInForm
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
            return redirect('signin')
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
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect email or password.')
        
    form = TeacherSignInForm()
    context = {
        'form': form
    }
    return render(request, 'teacher/signin.html', context)

def logoutTeacher(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'teacher/dashboard.html')
