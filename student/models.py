from django.db import models
from home.models import *
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    name  = models.CharField(max_length=30)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(SemesterDivision, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, null=True, blank=True)
    guardian = models.CharField(max_length=30, null=True, blank=True)
    guardian_phone = models.CharField(max_length=14, null=True, blank=True)
    guardian_email = models.EmailField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Leave(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_date = models.DateField()
    type = models.CharField(max_length=30)
    reason = models.CharField(max_length=40)
    note = models.TextField(blank=True, null=True)
    leave_time = models.TimeField(blank=True, null=True)
    faculty_approval = models.BooleanField(default=False)
    faculty_approval_time = models.DateTimeField(null=True, blank=True)
    hod_approval = models.BooleanField(default=False)
    hod_approval_time = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.type} on {self.leave_date}"
    
