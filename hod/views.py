from django.shortcuts import render, redirect
from .models import HOD
from home.models import Department
from student.models import *
from datetime import datetime, date
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.
def hod_dash(request):
    user = request.user
    hod = HOD.objects.get(user=user)
    print(hod.department)
    if not hod.department:
        return redirect('hod_profile')
    return render(request, 'hod/hod_dashboard.html', {'hod':hod})

def hod_profile(request):
    user = request.user
    hod = HOD.objects.get(user=user)
    departments = Department.objects.all()
    if request.method=="POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)

        hod.name = name
        hod.phone = phone
        hod.department = department
        hod.save()
        return redirect ('hod_dashboard')

    return render(request, 'hod/hod_profile.html', {'hod':hod, 'departments':departments})

def hod_full_day(request):
    user = request.user
    hod = HOD.objects.get(user=user)
    leaves = Leave.objects.filter(student__department = hod.department, type = 'Full day').order_by('-leave_date')
    todays_leaves = leaves.filter(leave_date=date.today())
    return render(request, 'hod/hod_full_day_leave.html', {'leaves':  leaves,'todays_leaves':todays_leaves})

def hod_half_day(request):
    user = request.user
    hod = HOD.objects.get(user=user)
    leaves = Leave.objects.filter(student__department=hod.department,  type="Half day", faculty_approval=True).order_by('-leave_date')
    todays_leaves = leaves.filter(leave_date=date.today())
    return render(request, 'hod/hod_half_day_leave.html', {'leaves':leaves, 'todays_leaves':todays_leaves})

def hod_half_day_approve(request, leave_id):
    user = request.user
    hod = HOD.objects.get(user=user)
    hod_name = hod.name
    hod_dept = hod.department.name
    leave = Leave.objects.get(id= leave_id)
    leave.hod_approval = True
    leave.hod_approval_time = timezone.now()
    qr_data = f"Gate Pass \n------------------------\nStudent: {leave.student.name}\nDate: {leave.leave_date}\nTime: {leave.leave_time}\nType: {leave.type}\nApproved by: \n\t{hod_name}\n\t{hod_dept}"
    print(qr_data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    leave.qr_code.save(f"gatepass_{leave.student.name}_{leave.leave_date}.png", File(buffer), save=False)

    leave.save()
    student = leave.student
    subject = 'Informing About leave request'

    # return render(request, 'hod/hod_inform_parent.html', {'student':student, 'subject':subject, 'leave':leave, 'hod':hod})
    try:
        html_message = render_to_string('hod/hod_inform_parent.html', {
                'student':student, 'subject':subject, 'leave':leave, 'hod':hod
            })
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [student.guardian_email]  

        send_mail(subject, 'OTP for registration', email_from, recipient_list, html_message=html_message)
    except Exception as e:
        print(f"Error sending email: {e}")
    return redirect('hod_half_day')

