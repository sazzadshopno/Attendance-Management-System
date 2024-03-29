from datetime import date, timedelta
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


class AttendanceForm(forms.Form):
    student_name = forms.CharField(max_length=255, required=False)
    student_id = forms.CharField(max_length=255, required=False)
    course_id = forms.CharField(max_length=255, required=False)
    roll_no = forms.CharField(max_length=10, required=False)
    status = forms.BooleanField(required=False)
    date = forms.CharField(required=False)


class AttendanceDateForm(forms.Form):
    date_choices = [(str(date.today() - timedelta(i)), (str(date.today() - timedelta(i)))) for i in range(7)]

    attendance_date = forms.ChoiceField(choices=tuple(date_choices))

    class Meta:
        fields = ["attendance_date"]
