from django.urls import path
from . import views

urlpatterns = [
    path('', views.hod_dash, name="hod_dashboard"),
    path('hod_profile', views.hod_profile, name="hod_profile"),
    path('hod_full_day', views.hod_full_day, name="hod_full_day"),
    path('hod_half_day', views.hod_half_day, name="hod_half_day"),
    path('hod_half_day_approve/<int:leave_id>', views.hod_half_day_approve, name="hod_half_day_approve"),
    

]
