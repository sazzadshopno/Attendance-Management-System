from django.forms import ModelForm
from .models import Teacher

class TeacherRegisterForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        ]