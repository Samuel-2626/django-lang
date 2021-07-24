from django.views.generic import ListView

from .models import Course


class ListCourse(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
