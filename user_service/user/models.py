from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from user.manager import CustomUserManager


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class User(AbstractUser): 
    phone_number = models.CharField(
        max_length=25,
        unique=True,
        validators=[phone_regex],
        db_index=True,
        verbose_name="phone number"
    )
    first_name = models.CharField(max_length=100, verbose_name="first name")
    last_name = models.CharField(max_length=100, verbose_name="last name")
    national_id = models.CharField(max_length=10, verbose_name="national id")
    username = None 

    USERNAME_FIELD = 'phone_number' 
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()
    
    def __str__(self): 
        return self.phone_number
