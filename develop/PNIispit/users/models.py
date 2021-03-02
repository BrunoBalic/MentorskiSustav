from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Users(AbstractUser):
    # override
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    # kada ovo promjenim za authentication1 mi se trazi email a ne username
    # kad ovo promjenim nije potrebna migracija, niti restart servera...
    USERNAME_FIELD = 'email'  # ovo je po defaultu required
    REQUIRED_FIELDS = ['username', ]

    # my fileds
    class UserRole(models.TextChoices):
        NONE = 'NONE', _('None')
        MENTOR = 'MENTOR', _('Mentor')
        STUDENT = 'STUDENT', _('Student')

    user_role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        null=False,
    )

    class Status(models.TextChoices):
        NONE = 'NONE', _('None')
        REDOVNI = 'REDOVNI', _('Redovni')
        IZVANREDNI = 'IZVANREDNI', _('Izvanredni')

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        null=False,
    )

    class Meta:
        verbose_name = _('Korisnik')
        verbose_name_plural = _('Korisnici')
