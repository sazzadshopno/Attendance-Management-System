from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user_name = models.CharField(max_length = 20, primary_key= True)
    password = models.CharField(max_length = 20)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Course(models.Model):
    code = models.CharField(max_length = 10, primary_key = True)
    title = models.CharField(max_length = 50)
    semester = models.CharField(max_length = 20)
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

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.student