from django.contrib import admin
from .models import Student
# Register your models here.


class StudenAdmin(admin.ModelAdmin):
    list_display=['id', 'rollno', 'name', 'address']

admin.site.register(Student, StudenAdmin)