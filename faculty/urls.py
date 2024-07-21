from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_dash, name="faculty_dashboard"),
    path('fac_full_day_leave', views.fac_full_day_leave, name="fac_full_day_leave"),
    path('fac_half_day_leave', views.fac_half_day_leave, name="fac_half_day_leave"),
    path('faculty_profile', views.faculty_profile, name="faculty_profile"),
    path('fac_approval/<int:leave_id>', views.fac_approval, name="fac_approval"),
    
    
    
]


