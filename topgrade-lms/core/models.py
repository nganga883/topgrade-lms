from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # for safe FK to custom User

# -----------------------------
# Custom User model
# -----------------------------
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_suspended = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# -----------------------------
# Course model
# -----------------------------
class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # safe reference to custom User
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'lecturer'}
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


# -----------------------------
# Material model (file uploads)
# -----------------------------
class Material(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Assignment(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assignments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')     

       
        