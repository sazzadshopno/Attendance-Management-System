from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Teacher

class TeacherBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            teacher = Teacher.objects.get(email=email)
            if check_password(password, teacher.password):
                return teacher
        except Teacher.DoesNotExist:
            return None