from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponseForbidden
from django.shortcuts import redirect 
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, CourseForm, SectionForm, LessonForm
from .models import Course, Section, Lesson, Enrollment, LessonProgress
from django.utils import timezone



User = get_user_model()


# регистрация и выход
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': RegisterForm()
            }
        return render(request, self.template_name, context)


    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        context = {'form': form}
        return render(request, self.template_name, context)
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


# отображение страниц
def index(request):
    return render(request, 'index.html', {index: 'index'})       

def courses(request):
    all_courses = Course.objects.all()
    return render(request, 'course_action/courses.html', {'courses': all_courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_action/course_detail.html', {'course': course})

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'lesson_action/lesson_detail.html', {'lesson': lesson})


# Действия с курсом
@login_required
def create_course(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("Только преподаватели могут создавать курсы.")
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            return redirect('courses')
    else:
        form = CourseForm()

    return render(request, 'course_action/create_course.html', {'form': form})

    

@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.creator:
        return HttpResponseForbidden("Вы не можете редактировать этот курс.")
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'course_action/edit_course.html', {'form': form})


@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user != course.creator:
        return HttpResponseForbidden("Вы не можете удалить этот курс.")
    
    if request.method == 'POST':
        course.delete()
        return redirect('courses')
    
    return redirect('course_detail', pk=course.pk)

# разделы уроков
@login_required
def add_section(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            return redirect('course_detail', pk=course_id)
    else:
        form = SectionForm()
    
    return render(request, 'section_action/add_section.html', {'form': form, 'course': course})

@login_required
def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.user != section.course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=section.course.id)
    else:
        form = SectionForm(instance=section)

    return render(request, 'section_action/edit_section.html', {'form': form, 'section': section})


@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    course_id = section.course.id
    if request.user != section.course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        section.delete()
        return redirect('course_detail', pk=course_id)

    return render(request, 'section_action/delete_section.html', {'section': section})


# Уроки
@login_required
def add_lesson(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.user != section.course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.section = section
            lesson.save()
            return redirect('course_detail', pk=section.course.id)
    else:
        form = LessonForm()

    return render(request, 'lesson_action/add_lesson.html', {'form': form, 'section': section})


@login_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.user != lesson.section.course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_detail', pk=lesson.section.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'lesson_action/edit_lesson.html', {'form': form, 'lesson': lesson})


@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.section.course.id
    if request.user != lesson.section.course.creator:
        return HttpResponseForbidden()

    if request.method == 'POST':
        lesson.delete()
        return redirect('course_detail', pk=course_id)

    return render(request, 'lesson_action/delete_lesson.html', {'lesson': lesson})


# Профиль студента
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden()
    enrolled_courses = request.user.enrolled_courses.all()  
    return render(request, 'profiles/student_dashboard.html', {
        'courses': enrolled_courses
    })

# Профиль преподавателя
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden()
    my_courses = Course.objects.filter(creator=request.user)
    return render(request, 'profiles/teacher_dashboard.html', {
        'courses': my_courses
    })

# Запись на курс
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'student':
        if course.students.count() >= course.max_students:
            # Можно вывести сообщение или перенаправить с ошибкой
            return render(request, 'course_action/course_detail.html', {
                'course': course,
                'error': 'Достигнуто максимальное количество студентов на курсе.'
            })
        request.user.enrolled_courses.add(course)
        return redirect('student_dashboard')
    return HttpResponseForbidden()

# выполнение урока
@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    enrollment = Enrollment.objects.filter(student=request.user, course=lesson.section.course).first()

    if not enrollment:
        return HttpResponseForbidden("Вы не записаны на этот курс.")

    progress, created = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    if not progress.completed:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()

    return redirect('lesson_detail', lesson_id=lesson.id)

