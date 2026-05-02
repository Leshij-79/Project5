from asyncio.windows_events import NULL

from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import CustomUser, UserPayment


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user2 = CustomUser.objects.get(id=2)
            user3 = CustomUser.objects.get(id=3)
            user4 = CustomUser.objects.get(id=4)

            course1 = Course.objects.get(id=1)
            course2 = Course.objects.get(id=2)
            course3 = Course.objects.get(id=3)

            lesson3 = Lesson.objects.get(id=3)
            lesson4 = Lesson.objects.get(id=4)
            lesson6 = Lesson.objects.get(id=6)
        except (CustomUser.DoesNotExist, Course.DoesNotExist, Lesson.DoesNotExist) as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при получении объектов: {e}"))
            return
        payments = [
            {"user": user2,
             "date_payment": "2026-01-14",
             "payment_course": course1,
             "payment_lesson": None,
             "payment": 5000,
             "payment_method": "cash"
            },
            {"user": user2,
             "date_payment": "2026-02-14",
             "payment_course": None,
             "payment_lesson": lesson4,
             "payment": 15000,
             "payment_method": "transfer"
            },
            {"user": user3,
             "date_payment": "2026-03-14",
             "payment_course": course2,
             "payment_lesson": None,
             "payment": 5000,
             "payment_method": "cash"
            },
            {"user": user3,
             "date_payment": "2026-04-14",
             "payment_course":  None,
             "payment_lesson": lesson6,
             "payment": 25000,
             "payment_method": "transfer"
            },
            {"user": user4,
             "date_payment": "2026-01-14",
             "payment_course": course3,
             "payment_lesson": None,
             "payment": 5000,
             "payment_method": "cash"
            },
            {"user": user4,
             "date_payment": "2026-01-14",
             "payment_course": None,
             "payment_lesson": lesson3,
             "payment": 5000,
             "payment_method": "transfer"
            },
        ]

        for payment_data in payments:
            payment, created = UserPayment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created payment for user: {payment_data}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists payment for user: {payment_data}"))
