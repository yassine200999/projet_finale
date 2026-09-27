from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User
from django.db import IntegrityError
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-e', '--email',type=str,help="Define a super user email")
        parser.add_argument('-p', '--password',type=str,help="Define a super user password")
        parser.add_argument('-fn', '--first_name',type=str,help="Define a super user first_name")
        parser.add_argument('-ln', '--last_name',type=str,help="Define a super user last_name")
    def handle(self,*args,**kwargs):
        try:
            email=kwargs['email']
            pw=kwargs['password']
            if not pw or not email:
                self.stdout.write(self.style.ERROR("all fildes"))
                return
            try:
                email = f'{email}'
                password= f'{pw}'
                first_name=kwargs.get('first_name')
                last_name=kwargs.get('last_name')
                admin =User.objects.create(
                    last_name=last_name,
                    first_name=first_name,
                    email=email,
                    password= make_password(password),
                    is_admin=True,
                    is_verified=True
                    )
                admin.save()
                self.stdout.write(self.style.SUCCESS('super user added successefuly'))
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f'ERROR:{str(e)}'))
            except Exception as e:
                 self.stdout.write(self.style.ERROR(f'An unexepted error occurred :{str(e)}')) 
        except IntegrityError as e:
             return "Error"+str(e)