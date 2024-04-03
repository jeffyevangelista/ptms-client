# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from businessUnit.models import BusinessUnit
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') == 'Admin':
            extra_fields['is_staff'] = True
            extra_fields['is_superuser'] = True

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)

    ROLES = [
        ('Encoder', 'Encoder'),
        ('Cost Controller', 'Cost Controller'),
        ('General Manager', 'General Manager'),
        ('Fund Custodian', 'Fund Custodian'),
        ('Admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='Admin')
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET_NULL, null=True) #if the user is custodian null the company
    is_staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    objects = UserManager()

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
