from django.contrib import admin
from .models import Teacher, Student, Batch, Course, Attendance

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(Attendance)