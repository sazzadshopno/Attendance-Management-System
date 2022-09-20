from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class TeacherManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
class Teacher(AbstractBaseUser):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50, unique = True)
    username = models.CharField(max_length = 20, primary_key= True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = TeacherManager()

    class Meta:
        ordering = ['first_name']


    def has_perm(self, perm, obj= None):
        return self.is_active
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return  self.username

class Batch(models.Model):
    semester_id = models.CharField(max_length = 20, primary_key = True, null = False)
    semester = models.CharField(max_length = 20)
    department = models.CharField(max_length = 20)

    class Meta:
        ordering = ['semester_id']
    
    def __str__(self):
        return "%s %s" % (self.department, self.semester)
    
class Course(models.Model):
    code = models.CharField(max_length = 10, primary_key = True)
    title = models.CharField(max_length = 50)
    semester = models.ForeignKey(Batch, on_delete= models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete= models.CASCADE)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.title

class Student(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    registration_no = models.CharField(max_length = 15, primary_key = True)
    roll_no = models.CharField(max_length = 10)
    session = models.CharField(max_length = 10)
    semester = models.ForeignKey(Batch, on_delete= models.CASCADE)
    attendances = models.ManyToManyField(Course, through='Attendance')

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()
    createdAt = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.date} - {self.course} - {self.student}'