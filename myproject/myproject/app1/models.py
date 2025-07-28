
from django.db import models

# Create your models here.
from django.db import models
import uuid
class Student(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('FY', 'First Year'),
        ('SY', 'Second Year'),
        ('BA', 'Bachelor'),
        ("FYM", "First Year Master's"),
        ("SYM", "Second Year Master's"),
        ('OTHER', 'Other'),
    ]

    MAJOR_CHOICES = [
        ('Engineering', 'Engineering'),
        ('Economics', 'Economics'),
        ('Law', 'Law'),
        ('Politics', 'Politics'),
        ('Medicine', 'Medicine'),
        ('Aviation', 'Aviation'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False )
    
    full_name = models.CharField(max_length=100 ,blank=False)
    email = models.EmailField(unique=True ,blank=False)
    password = models.CharField(max_length=128,blank=False)  # hashed password storage recommended
    education_level = models.CharField(max_length=5, choices=EDUCATION_LEVEL_CHOICES)
    major = models.CharField(max_length=20, choices=MAJOR_CHOICES)
    face_image = models.ImageField(upload_to='student_faces/')
   

    def __str__(self):
        return self.full_name


from django.db import models
import uuid
from django.contrib.auth.hashers import make_password

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)  # Will store hashed passwords

    def save(self, *args, **kwargs):
        # Hash the password if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Class(models.Model):
    MAJOR_CHOICES = [
        ('Engineering', 'Engineering'),
        ('Economics', 'Economics'),
        ('Law', 'Law'),
        ('Politics', 'Politics'),
        ('Medicine', 'Medicine'),
        ('Aviation', 'Aviation'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)  # e.g. "Math 101"
    major = models.CharField(max_length=100 , choices=MAJOR_CHOICES)  # e.g. "Engineering"
    teachers = models.ManyToManyField('Teacher', related_name='classes')

    def __str__(self):
        return f"{self.name} ({self.major})"




class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, related_name='attendances' ,null=True)
    class_attended = models.ForeignKey('Class', on_delete=models.SET_NULL, related_name='attendances',null=True)
    date = models.DateField(auto_now_add=True)
    isPresent = models.BooleanField(default=False)

    def __str__(self):
        status = "Present" if self.isPresent else "Absent"
        return f"{self.student.full_name} - {self.class_attended.name} - {self.date} - {status}"

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


# models.py
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class PasswordResetToken(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=1)  # token valid for 1 hour
