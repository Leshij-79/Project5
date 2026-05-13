from django.db import models

from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
        unique=True,
    )

    preview = models.ImageField(
        upload_to="media/course_preview",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
        default="media/course_preview/default.jpg",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание курса",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="course_owner",
        verbose_name="Владелец курса",
        help_text="Владелец курса",
    )

    price = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Стоимость курса",
        help_text="Укажите стоимость курса",
        default=0,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание урока",
    )

    preview = models.ImageField(
        upload_to="media/lesson_preview",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
        default="media/lesson_preview/default.jpg",
    )

    url_video = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course",
        verbose_name="Курс урока",
        help_text="Укажите курс урока",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="lesson_owner",
        verbose_name="Владелец урока",
        help_text="Владелец урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Subscriptions(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subs_course",
        verbose_name="Курс подписки",
        help_text="Подписка на курс",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subs_user",
        verbose_name="Пользователь",
        help_text="Пользователь",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["course", "user"]

    def __str__(self):
        return f"{self.course} {self.user}"


class CoursePayment(models.Model):
    STATUS_CHOICES = [
        ("open", "Оформление продолжается"),
        ("expired", "Срок оформления истек"),
        ("complete", "Оформление завершено"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="course_payment",
        verbose_name="Оплачиваемый курс",
        help_text="Укажите оплачиваемый курс",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_course_payment",
        verbose_name="Плательщик",
        help_text="Укажите плательщика",
    )

    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )

    session_id = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
    )

    link = models.URLField(
        max_length=600,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату курса",
        help_text="Укажите ссылку на оплату курса",
    )

    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
        verbose_name="Статус оплаты",
        help_text="Укажите статус оплаты",
    )


    class Meta:
        verbose_name = "Оплата курса"
        verbose_name_plural = "Оплаты курсов"
        ordering = ["course", "user"]

    def __str__(self):
        return f"{self.course} {self.user}"
