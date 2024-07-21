from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dash, name="student_dashboard"),
    path('student_profile', views.student_profile, name='student_profile'),
    path('stu_full_day_leave', views.stu_full_day_leave, name='stu_full_day_leave'),
    path('stu_half_day_leave', views.stu_half_day_leave, name='stu_half_day_leave'),
    path('delete_leave/<int:leave_id>', views.delete_leave, name='delete_leave'),
    
    
]
