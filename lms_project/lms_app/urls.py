# lms_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms_app.views import CourseViewSet, NoteViewSet, QuizViewSet, QuizResultViewSet, UserViewSet
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quiz_results', QuizResultViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/registration/', RegisterView.as_view(), name='register'),
    # Any other URL patterns
]
