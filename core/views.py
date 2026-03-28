from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import User, Course, Material, Assignment, Submission, Enrollment



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
# Student Login ONLY
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

        # ❌ Block lecturers
        if user.role == "lecturer":
            message = "Lecturers must use the lecturer login page."
            return render(request, "core/login.html", {"message": message})

        # ❌ Block admins
        if user.is_superuser or user.is_staff or user.role == "admin":
            message = "Admins must log in through the admin page."
            return render(request, "core/login.html", {"message": message})

        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return redirect("student_dashboard")
        else:
            message = "Incorrect password!"

    return render(request, "core/login.html", {"message": message})


# -----------------------
# Lecturer Login (NEW)
# -----------------------
def lecturer_login(request):
    message = ""

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            message = "Lecturer account not found!"
            return render(request, "core/lecturer_login.html", {"message": message})

        if user.is_suspended:
            message = "Your account is suspended! Contact admin."
            return render(request, "core/lecturer_login.html", {"message": message})

        # ✅ Only lecturers allowed
        if user.role != "lecturer":
            message = "This login page is for lecturers only."
            return render(request, "core/lecturer_login.html", {"message": message})

        # ✅ Must be activated by admin
        if not user.is_staff:
            message = "Lecturer not activated by admin."
            return render(request, "core/lecturer_login.html", {"message": message})

        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return redirect("lecturer_dashboard")
        else:
            message = "Incorrect password!"

    return render(request, "core/lecturer_login.html", {"message": message})


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

    query = request.GET.get('q')

    enrolled_courses_qs = Enrollment.objects.filter(student=request.user)
    enrolled_course_ids = enrolled_courses_qs.values_list('course_id', flat=True)

    # ✅ Only NOT enrolled courses
    if query:
        courses = Course.objects.filter(name__icontains=query).exclude(id__in=enrolled_course_ids)
    else:
        courses = Course.objects.exclude(id__in=enrolled_course_ids)

    # ✅ My courses
    my_courses = Course.objects.filter(id__in=enrolled_course_ids)

    # ✅ Materials for enrolled courses
    materials = Material.objects.filter(course__in=my_courses)

    return render(request, "core/student_dashboard.html", {
        "courses": courses,
        "my_courses": my_courses,
        "materials": materials,
    })
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
# Admin dashboard
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
            message = f"{user.username} status updated."

        elif action == "reset_password":
            new_password = request.POST.get("new_password")
            if new_password:
                user.password = make_password(new_password)
                user.save()
                message = f"Password reset for {user.username}"

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
    lecturer_login_link = request.build_absolute_uri("/lecturer-login/")

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
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role="lecturer",
                is_staff=True
            )
            message = "Lecturer created successfully!"

    return render(request, "core/create_lecturer.html", {
        "message": message,
        "lecturer_login_link": lecturer_login_link
    })


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

        lecturer = get_object_or_404(User, id=lecturer_id)
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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Course

@login_required
def lecturer_courses(request):
    if request.user.role != 'lecturer':
        return redirect('/')

    courses = Course.objects.filter(lecturer=request.user)
    return render(request, 'core/lecturer_courses.html', {'courses': courses})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import FileResponse
from .models import Course, Material, Assignment, Submission, Enrollment


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'file']


@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id, lecturer=request.user)

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            return redirect('lecturer_courses')
    else:
        form = MaterialForm()

    return render(request, 'core/upload_material.html', {'form': form, 'course': course})



from django.shortcuts import render, get_object_or_404
from .models import Assignment, Submission

def view_submissions(request, assignment_id):
    # Only allow lecturer to see submissions for their course
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'core/view_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Submission

@login_required
def grade_submission(request, submission_id):
    # Only lecturers should grade submissions
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        grade = request.POST.get('grade')
        submission.grade = grade
        submission.save()
        return redirect('view_submissions', assignment_id=submission.assignment.id)

    return render(request, 'core/grade_submission.html', {'submission': submission})

def course_list(request):
    from .models import Course

    query = request.GET.get('q')

    if query:
        courses = Course.objects.filter(name__icontains=query)
    else:
        courses = Course.objects.all()

    return render(request, 'core/course_list.html', {'courses': courses})

# =========================
# ENROLL COURSE
# =========================
from django.contrib import messages

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        messages.success(request, f"You have successfully enrolled in {course.name}")
    else:
        messages.info(request, "You are already enrolled in this course")

    return redirect('student_dashboard')  


# =========================
# MY COURSES
# =========================
@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'core/my_courses.html', {
        'enrollments': enrollments
    })


# =========================
# SUBMIT ASSIGNMENT
# =========================
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            sub, created = Submission.objects.get_or_create(
                assignment=assignment,
                student=request.user
            )
            sub.file = form.cleaned_data['file']
            sub.save()
            return redirect('my_courses')
    else:
        form = SubmissionForm()

    return render(request, 'core/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })


# =========================
# DOWNLOAD MATERIAL
# =========================
def download_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return FileResponse(material.file.open('rb'), as_attachment=True)