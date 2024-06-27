# lms_app/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
import openai
from .models import Course, CustomUser, Note, Quiz, QuizResult
from .serializers import CourseSerializer, UserSerializer, NoteSerializer, QuizSerializer, QuizResultSerializer

openai.api_key = 'sk-proj-eWaov7NRlQzcJc7Vmq2gT3BlbkFJLIwp2tYhx5ZrND5V31SF'

# UserViewSet for handling user-related operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow any user to access registration

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'})
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Course.objects.all()
        elif user.role == 'teacher':
            return Course.objects.filter(teacher=user)
        else:
            return Course.objects.filter(students__in=[user])

    def check_permission(self, request):
        if request.user.role not in ['admin', 'teacher']:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        return None

    def create(self, request, *args, **kwargs):
        response = self.check_permission(request)
        if response:
            return response
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = self.check_permission(request)
        if response:
            return response
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role == 'admin':
            return super().destroy(request, *args, **kwargs)
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        response = self.check_permission(request)
        if response:
            return response
        course = self.get_object()
        student = get_object_or_404(CustomUser, id=request.data.get('student_id'))
        course.students.add(student)
        return Response({'detail': 'Student added'})

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        response = self.check_permission(request)
        if response:
            return response
        course = self.get_object()
        student = get_object_or_404(CustomUser, id=request.data.get('student_id'))
        course.students.remove(student)
        return Response({'detail': 'Student removed'})

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role in ['admin', 'teacher']:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Generate notes for the following content: " + request.data['content'],
                max_tokens=500
            )
            request.data['content'] = response.choices[0].text.strip()
            return super().create(request, *args, **kwargs)
        else:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role in ['admin', 'teacher']:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Generate a quiz for the following content: " + request.data['content'],
                max_tokens=500
            )
            request.data['questions'] = response.choices[0].text.strip()
            return super().create(request, *args, **kwargs)
        else:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

class QuizResultViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role == 'student':
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Check the following quiz: " + request.data['answers'],
                max_tokens=500
            )
            request.data['score'] = int(response.choices[0].text.strip())
            return super().create(request, *args, **kwargs)
        else:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
