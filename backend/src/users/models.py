from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )
        user.is_superuser = False
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="email address",
        error_messages={"unique": "A user with that email already exists."},
    )
    username = models.CharField(blank=True, max_length=150, verbose_name="username")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()

    def owner(self):
        return self

    def __str__(self):
        return self.email
