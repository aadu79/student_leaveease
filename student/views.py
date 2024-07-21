from django.shortcuts import render, redirect
from student.models import Student, Leave
from home.models import *
from datetime import datetime, date

# Create your views here.

def student_dash(request):
    user = request.user
    student = Student.objects.get(user=user)
    if student.department and student.semester:
        return render(request, 'student/student_dashboard.html', {'student':student})
    
    else:
        return redirect('student_profile')
    
def student_profile(request):
    user = request.user
    student = Student.objects.get(user=user)
    departments =  Department.objects.all()
    semesters = SemesterDivision.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')
        semester_id = request.POST.get('semester')
        phone = request.POST.get('phone')
        guardian = request.POST.get('guardian')
        guardian_phone = request.POST.get('guardian_phone')
        guardian_email = request.POST.get('guardian_email')

        department = Department.objects.get(id=department_id)
        semester = SemesterDivision.objects.get(id=semester_id)
        
        student.name = name
        student.department = department
        student.semester = semester
        student.phone = phone
        student.guardian = guardian
        student.guardian_phone = guardian_phone
        student.guardian_email = guardian_email
        student.save()
        return redirect('student_dashboard')

    return render(request, 'student/student_profile.html', {'student':student, 'departments':departments, 'semesters':semesters})

def stu_full_day_leave(request):
    user = request.user
    student = Student.objects.get(user=user)
    if not student.department or not student.semester:
        return redirect('student_profile')
    leaves = Leave.objects.filter(student=student, type = 'Full day').order_by('-leave_date')
    if request.method == 'POST':
        leave_date = request.POST.get('leave_date')
        reason = request.POST.get('reason')
        note = request.POST.get('note')

        leave = Leave(
            student=student, leave_date=leave_date,
            type = 'Full day', reason=reason, note=note,
        )
        leave.save()
        return redirect('stu_full_day_leave')
    return render(request, 'student/student_stu_full_day_leave.html', {'leaves': leaves})

def stu_half_day_leave(request):
    user = request.user
    student = Student.objects.get(user=user)
    if not student.department or not student.semester:
        return redirect('student_profile')
    leaves = Leave.objects.filter(student=student, type = 'Half day').order_by('-leave_date')
    today = date.today()
    today_leave=Leave.objects.filter(student=student, type = 'Half day', leave_date=today).first()
    if request.method == 'POST':
        leave_datetime = request.POST.get('leave_date')
        reason = request.POST.get('reason')
        note = request.POST.get('note')

        leave_date = leave_datetime.split('T')[0]
        leave_time = leave_datetime.split('T')[1]

        print('leave_date', leave_date)
        print('leave_time', leave_time)

        leave = Leave(
            student=student, leave_date=leave_date, leave_time=leave_time,
            type = 'Half day', reason=reason, note=note,
        )
        leave.save()
        return redirect('stu_half_day_leave')
    return render(request, 'student/stu_half_day_leave.html', {'leaves':leaves, 'today_leave':today_leave})


def delete_leave(request, leave_id):
    leave = Leave.objects.get(id=leave_id)
    leave.delete()
    return redirect('stu_half_day_leave')