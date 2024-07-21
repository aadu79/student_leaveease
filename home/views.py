from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from student.models import Student
from faculty.models import Faculty
from hod.models import HOD
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


# Create your views here.

def index(request):
    user_type = None
    if request.user.is_authenticated:
        user = request.user
        if Student.objects.filter(user=user).exists():
            user_type = 'Student'
        elif Faculty.objects.filter(user=user).exists():
            user_type = 'Faculty'
        elif HOD.objects.filter(user=user).exists():
            user_type = 'HOD'
    return render(request, 'home/index.html', {'user_type': user_type})

def dashboard(request):
    user = request.user
    if Student.objects.filter(user=user).exists():
        return redirect('student_dashboard')
    elif Faculty.objects.filter(user=user).exists():
        return redirect('faculty_dashboard')
    elif HOD.objects.filter(user=user).exists():
        return redirect('hod_dashboard')


def login(request):
    user_type = request.GET.get('usertype')
    if user_type:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user_type == 'Student':
                    if Student.objects.filter(user=user).exists():
                        auth_login(request, user)
                        return redirect('index')
                    else:
                        return render(request, 'home/login.html', {'user_type':user_type, 'error': 'Invalid credentials'})
                elif user_type == 'Faculty':
                    if Faculty.objects.filter(user=user).exists():
                        auth_login(request, user)
                        return redirect('index')
                    else:
                        return render(request, 'home/login.html', {'user_type':user_type, 'error': 'Invalid credentials'})
                elif user_type == 'HOD':
                    if HOD.objects.filter(user=user).exists():
                        auth_login(request, user)
                        return redirect('index')
                    else:
                        return render(request, 'home/login.html', {'user_type':user_type, 'error': 'Invalid credentials'})
                else:
                    return render(request, 'home/login.html', {'user_type':user_type, 'error': 'Invalid credentials'})
            else:
                return render(request, 'home/login.html', {'user_type':user_type, 'error': 'Invalid credentials'})
        return render(request, 'home/login.html', {'user_type':user_type})
    
    
    return render(request, 'home/pre_login.html')


def register(request):
    user_type = request.GET.get('user_type')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')

        print(password, confirm_password)

        if password != confirm_password:
            return render(request, 'home/register.html', {'user_type': user_type, 'error': "Passwords didn't match"})
        if User.objects.filter(email=email).exists():
            return render(request, 'home/register.html', {'user_type': user_type, 'error': "This email already exists"})
        if User.objects.filter(username=username).exists():
            return render(request, 'home/register.html', {'user_type': user_type, 'error': "This username already exist"})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        
        if user_type == 'Student':
            student = Student(name=fullname, user=user)
            student.save()
        if user_type == 'Faculty':
            faculty = Faculty(name=fullname, user=user)
            faculty.save()
        if user_type == 'HOD':
            hod = HOD(name=fullname, user=user)
            hod.save()
        return redirect('index')
    return render(request, 'home/register.html', {'user_type': user_type})


def logout(request):
    auth_logout(request)
    return redirect('index')



