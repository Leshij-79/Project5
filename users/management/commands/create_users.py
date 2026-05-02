from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            {"username": "user1", "email": "user1@user1.ru", "password": "123", "is_active": True},
            {"username": "user2", "email": "user2@user2.ru", "password": "123", "is_active": True},
            {"username": "user3", "email": "user3@user3.ru", "password": "123", "is_active": True},
        ]

        for user_data in users:
            user, created = CustomUser.objects.get_or_create(**user_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user: {user_data}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists user: {user_data}"))
