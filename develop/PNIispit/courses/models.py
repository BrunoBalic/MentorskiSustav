from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Courses(models.Model):
    ime = models.CharField(max_length=255, null=False,)
    kod = models.CharField(max_length=16, null=False, unique=True,)
    program = models.TextField(null=False,)
    bodovi = models.IntegerField(null=False,)
    sem_redovni = models.IntegerField(null=False,)
    sem_izvanredni = models.IntegerField(null=False,)

    class Izborni(models.TextChoices):
        DA = 'DA', _('Da')
        NE = 'NE', _('Ne')

    izborni = models.CharField(max_length=8, choices=Izborni.choices, null=False,)

    def __str__(self):
        return self.ime + " (" + self.kod + ")"

    class Meta:
        verbose_name = "Predmet"
        verbose_name_plural = "Predmeti"
