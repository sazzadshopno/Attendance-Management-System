from django.shortcuts import render
from .forms import TeacherRegisterForm

def signupTeacher(request):
    form = TeacherRegisterForm()
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
    else: 
        form = TeacherRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'teacher/signup.html', context)

def signinTeacher(request):
    form = TeacherRegisterForm()
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
    else: 
        form = TeacherRegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'teacher/signin.html', context)