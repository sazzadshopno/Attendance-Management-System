from django.forms import ModelForm
from .models import Teacher

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
