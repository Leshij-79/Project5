from django.db import models


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

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = ("Курсы",)
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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = ("Уроки",)
        ordering = ["title"]

    def __str__(self):
        return self.title
