from django.urls import reverse
from icecream import ic
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import CustomUser


class CourseTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(
            username="testuser",
            email="testuser@testuser.ru",
            password="123"
        )
        self.course = Course.objects.create(
            title="testcourse",
            description="testcourse",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="testlesson",
            description="testlesson",
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """
        Тест на просмотр курса
        :return:
        """

        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data["title"],
            self.course.title
        )

    def test_course_create(self):
        """
        Тест на создание курса
        Создаётся второй курс
        :return:
        """

        url = reverse("lms:course-list")
        data = {
            "title": "testcourse 2",
            "description": "testcourse"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Course.objects.count(),
            2
        )

    def test_course_update(self):
        """
        Тест на частичное обновление данных курса
        Обновляется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})
        data = data = {
            "title": "testcourse 3",
            "description": "testcourse"
        }

        response = self.client.patch(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data["title"],
            "testcourse 3"
        )

    def test_course_delete(self):
        """
        Тест на удаление курса
        Удаялется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Course.objects.count(),
            0
        )

    def test_course_list(self):
        """
        Тест на список курсов
        :return:
        """

        url = reverse("lms:course-list")

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            data["count"],
            1
        )


# class LessonTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             username="testuser",
#             email="testuser@testuser.ru",
#             password="123"
#         )
#         self.course = Course.objects.create(
#             title="testcourse",
#             description="testcourse"
#         )
#         self.lesson = Lesson.objects.create(
#             title="testlesson",
#             description="testlesson",
#             course=self.course,
#             owner=self.user
#         )
#         self.client.force_authenticate(user=self.user)
#
#     def test_lesson_retrieve(self):
#         url = reverse("lms:lesson-retrieve", kwargs={"pk": self.lesson.pk})
#         lesson = Lesson.objects.create()
