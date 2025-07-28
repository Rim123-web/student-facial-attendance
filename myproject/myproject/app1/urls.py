from django.contrib import admin

from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from django.conf.urls.static import static

import os


# app1/urls.py

from django.urls import path
from .views import StudentSignup, StudentLogin,update_teacher, get_students_for_class,teacher_login,get_teacher_info, Get_classes_by_student_major, verify_face_and_mark_attendance, student_logout,teacher_logout,ContactMessageCreate,StudentDetailView,StudentUpdate,get_student_attendance,get_teacher_classes
from . import views
urlpatterns = [
    path('student/signup/', StudentSignup.as_view(), name='student-signup'),
    path('student/login/', StudentLogin.as_view(), name='student-login'),
    path('teacher/login/', views.teacher_login, name='teacher-login'),
    path('api/classes/<uuid:student_id>/', views.Get_classes_by_student_major, name='get_classes_by_major'),
    path('api/verify-attendance/', views.verify_face_and_mark_attendance, name='verify-attendance'),
    path('student/logout/', student_logout, name='student_logout'),
    path('teacher/logout/', teacher_logout, name='teacher_logout'),
    path('api/contact/', ContactMessageCreate.as_view(), name='contact-message-create'),
   path('api/archive-attendance/<uuid:student_id>/', get_student_attendance.as_view(), name='archive-attendance'),
   path('api/teacher/<uuid:teacher_id>/classes/', views.get_teacher_classes),
   path('api/teacher/<uuid:teacher_id>/update/', views.update_teacher, name='update_teacher'),

   path('api/class/<uuid:class_id>/students/', views.get_students_for_class, name="class-students"),
 

 path('api/teacher/<uuid:teacher_id>/info/', views.get_teacher_info, name='get_teacher_info'),
    # urls.py
path('students/parameters/<uuid:student_id>/', StudentDetailView.as_view(), name='student-detail'),
path('students/update/<uuid:pk>/', StudentUpdate.as_view(), name='student-update'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)