# urls.py
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register_student, name='register_student'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('generate-paper/<int:course_id>/<str:difficulty_level>/', views.generate_paper, name='generate_paper'),
    path('download-paper/<int:course_id>/<str:difficulty_level>/', views.download_paper, name='download_paper'),
    path('submit-paper/<int:course_id>/<str:difficulty_level>/', views.submit_paper, name='submit_paper'),
    path('view_submitted_papers/', views.view_submitted_papers, name='view_submitted_papers'),
path('download_submitted_paper/<int:submission_id>/', views.download_submitted_paper, name='download_submitted_paper'),
path('notifications/', views.view_notifications, name='view_notifications'),
path('logout/', views.logout_view, name='logout'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)