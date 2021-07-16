from django.urls import path
from .views import ListCourse

urlpatterns = [
    path('', ListCourse.as_view()),
]
