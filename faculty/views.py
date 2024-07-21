from django.shortcuts import render, redirect
from .models import Faculty
from home.models import *
from student.models import Student, Leave
from datetime import datetime, date
from django.utils import timezone

# Create your views here.
def faculty_dash(request):
    user = request.user
    faculty = Faculty.objects.get(user=user)
    if faculty.department and faculty.semester:
        return render(request, 'faculty/faculty_dashboard.html', {'faculty':faculty})
    else:
        return redirect('faculty_profile')
    
def faculty_profile(request):
    user = request.user
    faculty = Faculty.objects.get(user=user)
    departments =  Department.objects.all()
    semesters = SemesterDivision.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')
        semester_id = request.POST.get('semester')

        department = Department.objects.get(id=department_id)
        semester = SemesterDivision.objects.get(id=semester_id)
        
        faculty.name = name
        faculty.phone = phone
        faculty.department = department
        faculty.semester = semester
        faculty.save()
        return redirect('faculty_dashboard')

    return render(request, 'faculty/faculty_profile.html', {'faculty':faculty, 'departments':departments, 'semesters':semesters})
    

def fac_full_day_leave(request):
    user = request.user
    faculty = Faculty.objects.get(user=user)
    department = faculty.department
    semester = faculty.semester
    leaves = Leave.objects.filter(student__department=department, student__semester=semester, type="Full day").order_by('-leave_date')
    today = date.today()
    todays_leaves = leaves.filter(leave_date=today)
    return render(request, 'faculty/fac_full_day_leave.html', {'leaves':leaves, 'todays_leaves':todays_leaves})

def fac_half_day_leave(request):
    user = request.user
    faculty = Faculty.objects.get(user=user)
    department = faculty.department
    semester = faculty.semester
    leaves = Leave.objects.filter(student__department=department, student__semester=semester, type="Half day").order_by('-leave_date')
    today = date.today()
    todays_leaves = leaves.filter(leave_date=today)
    return render(request, 'faculty/fac_half_day_leave.html', {'leaves':leaves, 'todays_leaves':todays_leaves})

def fac_approval(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    leave.faculty_approval = True
    leave.faculty_approval_time = timezone.now()
    leave.save()
    return redirect('fac_half_day_leave')
    