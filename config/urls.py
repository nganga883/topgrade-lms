from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing
    path('', views.home, name='home'),

    # Auth
    path('register/', views.student_register, name='student_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboards
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('lecturer_dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),

    # Admin dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admin pages
    path('manage_users/', views.manage_users, name='manage_users'),
    path('create_lecturer/', views.create_lecturer, name='create_lecturer'),
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('student_courses/', views.student_courses, name='student_courses'),


    path('lecturer-login/', views.lecturer_login, name='lecturer_login'),
]

# Serve uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
