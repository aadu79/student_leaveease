from django.db import models
from home.models import *
from faculty.models import Faculty
from django.contrib.auth.models import User

# Create your models here.
class HOD(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=14, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - HOD {self.department}"