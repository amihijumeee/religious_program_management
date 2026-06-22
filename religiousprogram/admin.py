from django.contrib import admin
from .models import Instructor, Program, Registration, Feedback

admin.site.register(Instructor)
admin.site.register(Program)
admin.site.register(Registration)
admin.site.register(Feedback)
