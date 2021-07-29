from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Course

admin.site.register(Course, TranslatableAdmin)
