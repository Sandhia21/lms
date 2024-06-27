from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from lms_app.views import CourseViewSet, NoteViewSet, QuizViewSet, QuizResultViewSet, UserViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quizresults', QuizResultViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
