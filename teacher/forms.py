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
            'password',
            'is_active',
            'is_staff',
            'is_superuser'
        ]
