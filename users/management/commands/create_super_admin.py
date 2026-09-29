from django.core.management.base import BaseCommand
from django.db import IntegrityError
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-e', '--email', type=str, required=True, help='Define a super user email')
        parser.add_argument('-p', '--password', type=str, required=True, help='Define a super user password')
        parser.add_argument('-fn', '--first_name', type=str, default='', help='Define a super user first_name')
        parser.add_argument('-ln', '--last_name', type=str, default='', help='Define a super user last_name')

    def handle(self, *args, **kwargs):
        try:
            admin = User.objects.create_superuser(
                email=kwargs['email'],
                password=kwargs['password'],
                first_name=kwargs['first_name'],
                last_name=kwargs['last_name'],
                is_verified=True,
            )
            self.stdout.write(
                self.style.SUCCESS(f'super user added successfully: {admin.email}')
            )
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'ERROR: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
