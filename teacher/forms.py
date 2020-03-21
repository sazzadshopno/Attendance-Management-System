from django.forms import ModelForm, formset_factory
from django import forms
from .models import Teacher, Attendance

class TeacherSignUpForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]

class TeacherSignInForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'email',
            'password'
        ]


class AttendanceForm(ModelForm):
    student_name = forms.CharField(max_length=255, required=True)
    roll_no = forms.CharField(max_length=10, required = True)
    course_title = forms.CharField(max_length=255)
    class Meta:
        model = Attendance
        fields = '__all__'

