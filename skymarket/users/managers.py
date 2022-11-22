from django.contrib.auth.models import (BaseUserManager)


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, phone, password=None):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('Вы не ввели Email.')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,


        )

        user.role = 'user'
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        """
        Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError('Вы не ввели Email.')

        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password


        )

        user.role = 'admin'
        user.save(using=self._db)
        return user
