from django.contrib import admin
from .models import Teacher
from .models import Student
from .models import Class
from .models import Attendance
from .models import ContactMessage
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(ContactMessage)