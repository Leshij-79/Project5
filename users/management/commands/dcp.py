from django.core.management import BaseCommand

from users.models import UserPayment


class Command(BaseCommand):
    def handle(self, *args, **options):
        UserPayment.objects.all().delete()