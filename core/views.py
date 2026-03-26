from django.shortcuts import render, redirect, get_object_or_404
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
        elif User.objects.filter(email=email).exists():
            message = "Email already exists!"
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role="student"
            )
            return redirect("login")

    return render(request, "core/register.html", {"message": message})


# -----------------------
# Login view for students and lecturers only
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

        # block admins from custom login page
        if user.is_superuser or user.is_staff or user.role == "admin":
            message = "Admins must log in through the admin login page."
            return render(request, "core/login.html", {"message": message})

        if user.role == "lecturer" and not user.is_staff:
            message = "Lecturer account not yet added by admin!"
            return render(request, "core/login.html", {"message": message})

        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)

            if user_auth.role == "student":
                return redirect("student_dashboard")
            elif user_auth.role == "lecturer":
                return redirect("lecturer_dashboard")
            else:
                message = "This account cannot use this login page."
        else:
            message = "Incorrect password!"

    return render(request, "core/login.html", {"message": message})


# -----------------------
# Logout
# -----------------------
def user_logout(request):
    logout(request)
    return redirect("home")


# -----------------------
# Student dashboard
# -----------------------
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")

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
        return redirect("login")

    message = ""
    courses = Course.objects.filter(lecturer=request.user)
    materials = Material.objects.filter(course__lecturer=request.user)

    if request.method == "POST":
        course_id = request.POST.get("course")
        title = request.POST.get("title")
        file = request.FILES.get("file")

        course = get_object_or_404(Course, id=course_id, lecturer=request.user)
        Material.objects.create(title=title, file=file, course=course)
        message = "Material uploaded successfully!"

    return render(request, "core/lecturer_dashboard.html", {
        "courses": courses,
        "materials": materials,
        "message": message
    })


# -----------------------
# Custom admin dashboard
# -----------------------
def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/admin_dashboard/")

    if not request.user.is_superuser:
        logout(request)
        return redirect("/admin/login/?next=/admin_dashboard/")

    return render(request, "core/admin_dashboard.html")


# -----------------------
# Manage users
# -----------------------
def manage_users(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/manage_users/")

    if not request.user.is_superuser:
        logout(request)
        return redirect("/admin/login/?next=/manage_users/")

    users = User.objects.all()
    message = ""

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        if action == "toggle":
            user.is_suspended = not user.is_suspended
            user.save()
            message = f"{user.username} suspension status updated successfully."

        elif action == "reset_password":
            new_password = request.POST.get("new_password")
            if new_password:
                user.password = make_password(new_password)
                user.save()
                message = f"Password reset for {user.username}"
            else:
                message = "Please provide a new password."

    return render(request, "core/manage_users.html", {
        "users": users,
        "message": message
    })


# -----------------------
# Create lecturer
# -----------------------
def create_lecturer(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/create_lecturer/")

    if not request.user.is_superuser:
        logout(request)
        return redirect("/admin/login/?next=/create_lecturer/")

    message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            message = "Username already exists!"
        elif User.objects.filter(email=email).exists():
            message = "Email already exists!"
        else:
            User.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=make_password(password),
                role="lecturer",
                is_staff=True
            )
            message = "Lecturer created successfully!"

    return render(request, "core/create_lecturer.html", {"message": message})


# -----------------------
# Manage courses
# -----------------------
def manage_courses(request):
    if not request.user.is_authenticated:
        return redirect("/admin/login/?next=/manage_courses/")

    if not request.user.is_superuser:
        logout(request)
        return redirect("/admin/login/?next=/manage_courses/")

    courses = Course.objects.all()
    lecturers = User.objects.filter(role="lecturer")
    message = ""

    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        lecturer_id = request.POST.get("lecturer")

        lecturer = get_object_or_404(User, id=lecturer_id, role="lecturer")
        Course.objects.create(name=name, code=code, lecturer=lecturer)
        message = "Course added successfully."

    return render(request, "core/manage_courses.html", {
        "courses": courses,
        "lecturers": lecturers,
        "message": message
    })


# -----------------------
# Student courses
# -----------------------
@login_required
def student_courses(request):
    if request.user.role != "student":
        return redirect("login")

    courses = Course.objects.all()
    materials = Material.objects.all()

    return render(request, "core/student_courses.html", {
        "courses": courses,
        "materials": materials
    })