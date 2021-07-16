from django.contrib import admin
from .models import Course

from parler.admin import TranslatableAdmin

# Register your models here.

admin.site.register(Course, TranslatableAdmin)
