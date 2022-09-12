from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('teacher.urls'))
]

admin.site.site_header = 'TEACHERS ADMIN'