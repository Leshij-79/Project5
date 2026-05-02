from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    EMAIL_FIELD = "email"

    avatar = models.ImageField(upload_to="media/avatars", blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(blank=True, null=True, max_length=15, verbose_name="Номер телефона")
    city = models.CharField(blank=True, null=True, max_length=50, verbose_name="Город")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class UserPayment(models.Model):
    METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт")
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_payment",
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )

    date_payment = models.DateField(
        verbose_name="Дата оплаты",
        help_text="Укажите дату оплаты",
    )

    payment_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payment_course",
        blank=True,
        null=True,
        verbose_name="Оплата курса",
        help_text="Укажите оплаченный курс",
    )

    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="payment_lesson",
        blank=True,
        null=True,
        verbose_name="Оплата урока",
        help_text="Укажите оплаченный урок",
    )

    payment = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )

    payment_method = models.CharField(
        max_length=8,
        choices=METHOD_CHOICES,
        default="transfer",
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )

    class Meta:
        verbose_name = ""
        verbose_name_plural = ""
        ordering = ["user", "-date_payment"]

    def __str__(self):
        return self.user
