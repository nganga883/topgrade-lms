from django.urls import path
from . import views

urlpatterns = [
    path('lecturer/courses/', views.lecturer_courses, name='lecturer_courses'),
    path('upload-material/<int:course_id>/', views.upload_material, name='upload_material'),

    path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),

    path('courses/', views.course_list, name='course_list'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),

    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('download/<int:material_id>/', views.download_material, name='download_material'),

    path('available-courses/', views.available_courses, name='available_courses'),
    path('my-courses/', views.my_courses, name='my_courses'),
]