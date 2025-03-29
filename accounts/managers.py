from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('فیلد username باید مقدار داشته باشد.')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # فرض بر این است که سوپر یوزر از نوع manager است.
        extra_fields.setdefault('user_type', 'manager')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('user_type') != 'manager':
            raise ValueError('سوپر یوزر باید از نوع manager باشد.')
        if not extra_fields.get('is_staff'):
            raise ValueError('سوپر یوزر باید is_staff=True داشته باشد.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('سوپر یوزر باید is_superuser=True داشته باشد.')

        return self.create_user(username, password, **extra_fields)