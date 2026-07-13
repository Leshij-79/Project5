from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscriptions
from users.models import CustomUser


class CourseTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(username="testuser", email="testuser@testuser.ru", password="123")

        self.course = Course.objects.create(
            title="testcourse", description="testcourse", preview=None, owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="testlesson", description="testlesson", preview=None, course=self.course, owner=self.user
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], self.course.title)

    def test_course_create(self):
        """
        Тест на создание курса
        Создаётся второй курс
        :return:
        """

        url = reverse("lms:course-list")
        data = {"title": "testcourse 2", "description": "testcourse"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.count(), 2)

    def test_course_update(self):
        """
        Тест на частичное обновление данных курса
        Обновляется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})
        data = data = {"title": "testcourse 3", "description": "testcourse"}

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], "testcourse 3")

    def test_course_delete(self):
        """
        Тест на удаление курса
        Удаляется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.count(), 0)

    def test_course_list(self):
        """
        Тест на список курсов
        :return:
        """

        url = reverse("lms:course-list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "count": 1,
                    "course": [
                        {
                            "course": self.course.pk,
                            "description": self.lesson.description,
                            "id": self.lesson.pk,
                            "owner": self.user.pk,
                            "preview": None,
                            "title": self.lesson.title,
                            "url_video": None,
                        }
                    ],
                    "description": self.course.description,
                    "id": self.course.pk,
                    "owner": self.user.pk,
                    "preview": None,
                    "price": 0,
                    "subs_course": 0,
                    "title": self.course.title,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)

        self.assertEqual(data, result)


class LessonTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(username="testuser", email="testuser@testuser.ru", password="123")
        self.course = Course.objects.create(
            title="testcourse", description="testcourse", preview=None, owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="testlesson",
            description="testlesson",
            preview=None,
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """
        Тест на просмотр урока
        :return:
        """

        url = reverse("lms:lesson-retrieve", kwargs={"pk": self.lesson.pk})

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], self.lesson.title)

    def test_lesson_create(self):
        """
        Тест на создание урока
        Создаётся второй урок
        :return:
        """

        url = reverse("lms:lesson-create")
        data = {
            "title": "testlesson 2",
            "description": "testlesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        """
        Тест на частичное обновление данных урока
        Обновляется первый урок
        :return:
        """
        url = reverse("lms:lesson-update", kwargs={"pk": self.lesson.pk})
        data = data = {"title": "testlesson 3", "description": "testlesson"}

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], "testlesson 3")

    def test_lesson_delete(self):
        """
        Тест на удаление урока
        Удаляется первый урок
        :return:
        """
        url = reverse("lms:lesson-destroy", kwargs={"pk": self.lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        """
        Тест на список уроков
        :return:
        """

        url = reverse("lms:lesson-list")

        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "course": self.course.pk,
                    "description": self.lesson.description,
                    "id": self.lesson.pk,
                    "owner": self.user.pk,
                    "preview": None,
                    "title": self.lesson.title,
                    "url_video": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)

        self.assertEqual(data, result)


class CourseModeratorTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(username="testuser", email="testuser@testuser.ru", password="123")
        group, created = Group.objects.get_or_create(name="Moderator")
        self.user.groups.add(group)

        self.course = Course.objects.create(
            title="testcourse", description="testcourse", preview=None, owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="testlesson", description="testlesson", preview=None, course=self.course, owner=self.user
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], self.course.title)

    def test_course_create(self):
        """
        Тест на создание курса
        Создаётся второй курс
        :return:
        """

        url = reverse("lms:course-list")
        data = {"title": "testcourse 2", "description": "testcourse"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update(self):
        """
        Тест на частичное обновление данных курса
        Обновляется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})
        data = data = {"title": "testcourse 3", "description": "testcourse"}

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], "testcourse 3")

    def test_course_delete(self):
        """
        Тест на удаление курса
        Удаляется первый курс
        :return:
        """
        url = reverse("lms:course-detail", kwargs={"pk": self.course.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_list(self):
        """
        Тест на список курсов
        :return:
        """

        url = reverse("lms:course-list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "count": 1,
                    "course": [
                        {
                            "course": self.course.pk,
                            "description": self.lesson.description,
                            "id": self.lesson.pk,
                            "owner": self.user.pk,
                            "preview": None,
                            "title": self.lesson.title,
                            "url_video": None,
                        }
                    ],
                    "description": self.course.description,
                    "id": self.course.pk,
                    "owner": self.user.pk,
                    "preview": None,
                    "price": 0,
                    "subs_course": 0,
                    "title": self.course.title,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)

        self.assertEqual(data, result)


class LessonModeratorTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(username="testuser", email="testuser@testuser.ru", password="123")
        group, created = Group.objects.get_or_create(name="Moderator")
        self.user.groups.add(group)

        self.course = Course.objects.create(
            title="testcourse", description="testcourse", preview=None, owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="testlesson",
            description="testlesson",
            preview=None,
            course=self.course,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """
        Тест на просмотр урока
        :return:
        """

        url = reverse("lms:lesson-retrieve", kwargs={"pk": self.lesson.pk})

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], self.lesson.title)

    def test_lesson_create(self):
        """
        Тест на создание урока
        Создаётся второй урок
        :return:
        """

        url = reverse("lms:lesson-create")
        data = {
            "title": "testlesson 2",
            "description": "testlesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        """
        Тест на частичное обновление данных урока
        Обновляется первый урок
        :return:
        """
        url = reverse("lms:lesson-update", kwargs={"pk": self.lesson.pk})
        data = data = {"title": "testlesson 3", "description": "testlesson"}

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["title"], "testlesson 3")

    def test_lesson_delete(self):
        """
        Тест на удаление урока
        Удаляется первый урок
        :return:
        """
        url = reverse("lms:lesson-destroy", kwargs={"pk": self.lesson.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        """
        Тест на список уроков
        :return:
        """

        url = reverse("lms:lesson-list")

        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "course": self.course.pk,
                    "description": self.lesson.description,
                    "id": self.lesson.pk,
                    "owner": self.user.pk,
                    "preview": None,
                    "title": self.lesson.title,
                    "url_video": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data["count"], 1)

        self.assertEqual(data, result)


class SubscriptionsTestCase(APITestCase):

    def setUp(self):
        """
        Предварительные настройки теста
        """

        self.user = CustomUser.objects.create(username="testuser", email="testuser@testuser.ru", password="123")

        self.course = Course.objects.create(
            title="testcourse", description="testcourse", preview=None, owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        """
        Тест на подписку и отписку от курс
        :return:
        """

        url = reverse("lms:subscription", kwargs={"pk": self.course.pk})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Subscriptions.objects.count(), 1)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Subscriptions.objects.count(), 0)
