from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Course, Material

# -----------------------
# Landing page
# -----------------------
def home(request):
    return render(request, 'core/home.html')


# -----------------------
# Student registration
# -----------------------
def student_register(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        confirm_email = request.POST.get("confirm_email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if email != confirm_email:
            message = "Emails do not match!"
        elif password1 != password2:
            message = "Passwords do not match!"
        elif User.objects.filter(username=username).exists():
            message = "Username already exists!"
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role="student"
            )
            return redirect("/login/")

    return render(request, "core/register.html", {"message": message})


# -----------------------
# Login view
# -----------------------
def user_login(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = "Email not found!"
            return render(request, "core/login.html", {"message": message})

        if user.is_suspended:
            message = "Your account is suspended! Contact admin."
            return render(request, "core/login.html", {"message": message})

        if user.role == "lecturer" and not user.is_staff:
            message = "Lecturer account not yet added by admin!"
            return render(request, "core/login.html", {"message": message})

        user_auth = authenticate(username=user.username, password=password)
        if user_auth:
            login(request, user_auth)
            if user.role == "student":
                return redirect("/student_dashboard/")
            elif user.role == "lecturer":
                return redirect("/lecturer_dashboard/")
            elif user.role == "admin":
                return redirect("/admin_dashboard/")
        else:
            message = "Incorrect password!"

    return render(request, "core/login.html", {"message": message})


# -----------------------
# Logout
# -----------------------
def user_logout(request):
    logout(request)
    return redirect('home')


# -----------------------
# Student dashboard
# -----------------------
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("/login/")

    context = {
        "num_courses": 5,
        "pending_assignments": 2,
        "class_schedule": "Mon, Wed, Fri - 10:00 AM to 12:00 PM",
        "notifications": 3,
        "announcements": [
            "Welcome to TOPGRADE LMS!",
            "Assignment 1 due next week.",
            "New lecture uploaded for Calculus."
        ]
    }
    return render(request, "core/student_dashboard.html", context)


# -----------------------
# Lecturer dashboard
# -----------------------
@login_required
def lecturer_dashboard(request):
    if request.user.role != "lecturer":
        return redirect("/login/")

    message = ""
    courses = Course.objects.filter(lecturer=request.user)
    materials = Material.objects.filter(course__lecturer=request.user)

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title")
        file = request.FILES.get("file")

        course = Course.objects.get(id=course_id)
        Material.objects.create(title=title, file=file, course=course)
        message = "Material uploaded successfully!"

    return render(request, "core/lecturer_dashboard.html", {
        "courses": courses,
        "materials": materials,
        "message": message
    })


# -----------------------
# Admin pages (custom login)
# -----------------------
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("/login/")
    return render(request, 'core/admin_dashboard.html')


@login_required
def manage_users(request):
    if request.user.role != "admin":
        return redirect("/login/")
    users = User.objects.all()
    message = ''

    if request.method == "POST":
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        if action == 'toggle':
            user.is_suspended = not user.is_suspended
            user.save()
        elif action == 'reset_password':
            new_password = request.POST.get('new_password')
            user.password = make_password(new_password)
            user.save()
            message = f"Password reset for {user.username}"

    return render(request, 'core/manage_users.html', {'users': users, 'message': message})


@login_required
def create_lecturer(request):
    if request.user.role != 'admin':
        return redirect('/login/')   # block non-admins

    message = ''
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        User.objects.create(
            username=username,
            email=email,
            phone=phone,
            password=make_password(password),
            role='lecturer',
            is_staff=True
        )
        message = 'Lecturer created successfully!'

    return render(request, 'core/create_lecturer.html', {'message': message})

@login_required
def manage_courses(request):
    if request.user.role != "admin":
        return redirect("/login/")
    courses = Course.objects.all()
    lecturers = User.objects.filter(role='lecturer')
    message = ''

    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        lecturer_id = request.POST.get('lecturer')
        lecturer = User.objects.get(id=lecturer_id)

        Course.objects.create(name=name, code=code, lecturer=lecturer)
        message = 'Course added successfully!'

    return render(request, 'core/manage_courses.html', {'courses': courses, 'lecturers': lecturers, 'message': message})
    
@login_required
def student_courses(request):
    if request.user.role != "student":
        return redirect("/login/")

    courses = Course.objects.all()
    materials = Material.objects.all()

    return render(request, "core/student_courses.html", {
        "courses": courses,
        "materials": materials
    })    
