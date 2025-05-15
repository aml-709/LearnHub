from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    # Регистрация и выход
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Профили Студента и Преподавателя
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    # Курсы
    path('courses/', views.courses, name='courses'),
    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<int:pk>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:pk>/', views.delete_course, name='delete_course'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    # Разделы
    path('course/<int:course_id>/add_section/', views.add_section, name='add_section'),
    path('section/<int:section_id>/edit/', views.edit_section, name='edit_section'),
    path('section/<int:section_id>/delete/', views.delete_section, name='delete_section'),
    # Уроки
    path('section/<int:section_id>/add_lesson/', views.add_lesson, name='add_lesson'),
    path('lesson/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('lesson/<int:lesson_id>/delete/', views.delete_lesson, name='delete_lesson'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    # Прогресс
    path('lesson/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    # Запись на курс
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),

] 

# для обработки медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)