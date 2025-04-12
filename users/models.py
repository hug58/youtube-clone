from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,  
        blank=False,  
        null=False,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )

    USERNAME_FIELD = 'username'  
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
