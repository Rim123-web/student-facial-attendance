from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Student

from .models import Teacher
from .Serializers import StudentSerializer

# class StudentSignup(APIView):
#     def post(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.parsers import MultiPartParser, FormParser

class StudentSignup(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            student = Student.objects.get(email=email)
            if check_password(password, student.password):
                return Response({
                    'message': 'Login successful',
                    'id': str(student.id),  # ✅ this is what your frontend needs!
                    'full_name': student.full_name,
                    'email': student.email
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)






import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import Teacher

@csrf_exempt
def teacher_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            teacher = Teacher.objects.get(email=email)
        except Teacher.DoesNotExist:
            return JsonResponse({"error": "Invalid email or password."}, status=400)

        if not check_password(password, teacher.password):
            return JsonResponse({"error": "Invalid email or password."}, status=400)

        # Success: return teacher info including id as string
        return JsonResponse({
            "id": str(teacher.id),  # Important: return as string
            "name": teacher.name,
            "email": teacher.email,
        })

    return JsonResponse({"error": "Only POST allowed"}, status=405)



from django.http import JsonResponse
from .models import Class, Student

def Get_classes_by_student_major(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        classes = Class.objects.filter(major=student.major)
        class_list = [
            {
                "id": str(c.id),
                "name": c.name,
                "major": c.major,
                "teachers": [t.name for t in c.teachers.all()],
            }
            for c in classes
        ]
        return JsonResponse({"status": "success", "classes": class_list}, status=200)
    except Student.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Student not found"}, status=404)




# views.py
import face_recognition
from django.http import JsonResponse
from .models import Student, Class, Attendance
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import io
from PIL import Image
from django.utils.timezone import now

@csrf_exempt
def verify_face_and_mark_attendance(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    student_id = request.POST.get('student_id')
    class_id = request.POST.get('class_id')
    image_data = request.POST.get('image')  # base64 image from frontend

    if not all([student_id, class_id, image_data]):
        return JsonResponse({"error": "Missing data"}, status=400)

    try:
        student = Student.objects.get(id=student_id)
        class_obj = Class.objects.get(id=class_id)

        # Load registered face
        student_face_path = student.face_image.path
        registered_image = face_recognition.load_image_file(student_face_path)
        registered_encoding = face_recognition.face_encodings(registered_image)[0]

        # Load image from base64 webcam capture
        format, imgstr = image_data.split(';base64,')
        img_bytes = base64.b64decode(imgstr)
        img = Image.open(io.BytesIO(img_bytes))
        webcam_image = face_recognition.load_image_file(io.BytesIO(img_bytes))
        webcam_encodings = face_recognition.face_encodings(webcam_image)

        if not webcam_encodings:
            return JsonResponse({"error": "No face detected in webcam image"}, status=400)

        webcam_encoding = webcam_encodings[0]

        # Compare
        results = face_recognition.compare_faces([registered_encoding], webcam_encoding)
        if results[0]:
            today = now().date()
            attendance_exists = Attendance.objects.filter(
                student=student,
                class_attended=class_obj,
                date=today,
            ).exists()

            if attendance_exists:
                return JsonResponse({"status": "success", "message": "Attendance already marked for today"})

            Attendance.objects.create(
                student=student,
                class_attended=class_obj,
                isPresent=True
            )
            return JsonResponse({"status": "success", "message": "Attendance marked as present"})
        else:
            return JsonResponse({"status": "fail", "message": "Face not recognized"})

    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"}, status=404)
    except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Logout student


# views.py
from rest_framework import generics
from .models import Attendance
from .Serializers import AttendanceSerializer

class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


@csrf_exempt
def student_logout(request):
    if request.method == 'POST':
        try:
            request.session.flush()  # Clears the session data
            return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    return JsonResponse({'status': 'failed', 'message': 'Only POST method allowed'}, status=405)



# logout teacher

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def teacher_logout(request):
    if request.method == 'POST':
        try:
            request.session.flush()  # Clears the session data
            return JsonResponse({'status': 'success', 'message': 'Logged out successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    return JsonResponse({'status': 'failed', 'message': 'Only POST method allowed'}, status=405)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializers import ContactMessageSerializer

class ContactMessageCreate(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py
class StudentDetailView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)



class StudentUpdate(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .Serializers import AttendanceSerializer

class get_student_attendance(APIView):
    def get(self, request, student_id):
        try:
            attendance_records = Attendance.objects.filter(student__id=student_id)
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Class
from .Serializers import ClassSerializer

class ClassListAPIView(APIView):
    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    
from django.http import JsonResponse
from .models import Teacher

def get_teacher_classes(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        classes = teacher.classes.all()
        data = [
            {
                "id": str(cls.id),
                "name": cls.name,
                "major": cls.major
            }
            for cls in classes
        ]
        return JsonResponse(data, safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)



from django.http import JsonResponse
from .models import Teacher

def get_teacher_info(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        data = {
            "name": teacher.name,
            "email": teacher.email
        }
        return JsonResponse(data)
    except Teacher.DoesNotExist:
        return JsonResponse({"error": "Teacher not found"}, status=404)
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher
from .Serializers import TeacherSerializer

@api_view(['PATCH'])
def update_teacher(request, teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherSerializer(teacher, data=request.data, partial=True)  # Allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.http import JsonResponse
from .models import Attendance
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_students_for_class(request, class_id):
    if request.method == "GET":
        attendance_records = Attendance.objects.filter(class_attended__id=class_id).select_related("student", "class_attended")

        result = []
        for record in attendance_records:
            if record.student:  # check student exists
                result.append({
                    "student_name": record.student.full_name,
                    "major": record.student.major,
                    "class_name": record.class_attended.name,
                    "is_present": record.isPresent,
                     "date": record.date.strftime("%Y-%m-%d"),
                })
        return JsonResponse(result, safe=False)



from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import Student  # replace 'yourapp' with your app name
# views.py
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, PasswordResetToken
from django.utils import timezone

# @csrf_exempt
# def forgot_password(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         email = data.get("email", "").strip()

#         try:
#             student = Student.objects.get(email=email)
#         except Student.DoesNotExist:
#             return JsonResponse({"error": "Email not found."}, status=400)

#         # Create a password reset token
#         reset_token = PasswordResetToken.objects.create(student=student)

#         reset_link = f"http://yourdomain.com/reset-password/{reset_token.token}/"

#         # Send reset email
#         send_mail(
#             subject="Password Reset Request",
#             message=f"Hello {student.full_name},\n\nUse the link below to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email.",
#             from_email="noreply@yourdomain.com",
#             recipient_list=[email],
#             fail_silently=False,
#         )

#         return JsonResponse({"message": "Password reset email sent."})

#     return JsonResponse({"error": "Invalid request method."}, status=405)




# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import json

# # views.py
# from django.shortcuts import render
# from django.contrib.auth.hashers import make_password

# @csrf_exempt
# def reset_password(request, token):
#     try:
#         reset_token = PasswordResetToken.objects.get(token=token)
#     except PasswordResetToken.DoesNotExist:
#         return JsonResponse({"error": "Invalid token."}, status=400)

#     if reset_token.is_expired():
#         return JsonResponse({"error": "Token expired."}, status=400)

#     if request.method == "POST":
#         data = json.loads(request.body)
#         new_password = data.get("new_password", "").strip()
#         if not new_password:
#             return JsonResponse({"error": "Password is required."}, status=400)

#         # Hash and update the student's password
#         reset_token.student.password = make_password(new_password)
#         reset_token.student.save()

#         # Optionally delete the token after use
#         reset_token.delete()

#         return JsonResponse({"message": "Password reset successfully."})

#     # For GET request, render a reset password HTML page (or send instructions)
#     # You can serve an HTML page with a form here if you want
#     return render(request, "reset_password_form.html", {"token": token})

