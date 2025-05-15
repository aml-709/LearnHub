from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course, Section, Lesson
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher',
            password='pass',
            role='teacher',
            email='teacher@example.com'
        )
        self.student = User.objects.create_user(
            username='student',
            password='pass',
            role='student',
            email='student@example.com'
        )
        self.course = Course.objects.create(title='Курс', description='Описание', creator=self.teacher)
        self.section = Section.objects.create(title='Раздел', course=self.course)
        self.lesson = Lesson.objects.create(title='Урок', content='Контент', section=self.section)

    def test_course_str(self):
        self.assertEqual(str(self.course), 'Курс')

    def test_section_str(self):
        self.assertEqual(str(self.section), 'Раздел')

    def test_lesson_str(self):
        self.assertEqual(str(self.lesson), 'Урок')

class ViewTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', password='pass', role='teacher', email='teacher@example.com'
        )
        self.student = User.objects.create_user(
            username='student', password='pass', role='student', email='student@example.com'
        )
        self.course = Course.objects.create(title='Курс', description='Описание', creator=self.teacher)
        self.section = Section.objects.create(title='Раздел', course=self.course)
        self.lesson = Lesson.objects.create(title='Урок', content='Контент', section=self.section)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_courses_view(self):
        response = self.client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Курс')

    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.title)

    def test_create_course_get_post(self):
        self.client.login(username='teacher', password='pass')
        get_response = self.client.get(reverse('create_course'))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('create_course'), {'title': 'Тест', 'description': 'desc'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Course.objects.filter(title='Тест').exists())

    def test_create_course_forbidden(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('create_course'))
        self.assertEqual(response.status_code, 403)

    def test_edit_course_get_post(self):
        self.client.login(username='teacher', password='pass')
        get_response = self.client.get(reverse('edit_course', args=[self.course.id]))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('edit_course', args=[self.course.id]), {'title': 'Изменено', 'description': 'desc'})
        self.assertEqual(post_response.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Изменено')

    def test_edit_course_forbidden(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('edit_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_delete_course_post(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.post(reverse('delete_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_delete_course_forbidden(self):
        self.client.login(username='student', password='pass')
        response = self.client.post(reverse('delete_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_add_section_get_post(self):
        self.client.login(username='teacher', password='pass')
        get_response = self.client.get(reverse('add_section', args=[self.course.id]))
        self.assertEqual(get_response.status_code, 200)
        post_response = self.client.post(reverse('add_section', args=[self.course.id]), {'title': 'Раздел 2'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Section.objects.filter(title='Раздел 2').exists())

    def test_add_section_forbidden(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('add_section', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)

    def test_lesson_detail_view(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('lesson_detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.lesson.title)

    def test_student_dashboard_view(self):
        self.client.login(username='student', password='pass')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_dashboard_view(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_enroll_course(self):
        self.client.login(username='student', password='pass')
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.course in self.student.enrolled_courses.all())

    def test_enroll_course_forbidden(self):
        self.client.login(username='teacher', password='pass')
        response = self.client.post(reverse('enroll_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)