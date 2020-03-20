from django.shortcuts import render, redirect
from .forms import TeacherSignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def signupTeacher(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if(form.is_valid()):
            teacher = form.save(commit=False)
            email = form.cleaned_data['email']
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

def signinTeacher(request):
    if request.method == 'POST':        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect email or password.')

    return render(request, 'teacher/signin.html')

def logoutTeacher(request):
    logout(request)
    return redirect('signin')

def dashboard(request):
    return render(request, 'teacher/dashboard.html')
