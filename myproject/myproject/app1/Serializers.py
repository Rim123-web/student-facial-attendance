# serializers.py
from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import make_password

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash the password
        return super().create(validated_data)

from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', default='')
    class_name = serializers.CharField(source='class_attended.name', default='')

    class Meta:
        model = Attendance
        fields = ['student_name', 'class_name', 'date', 'isPresent']


# serializers.py
from rest_framework import serializers
from .models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'major']

# serializers.py

from rest_framework import serializers
from .models import Teacher
from django.contrib.auth.hashers import make_password

class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)

