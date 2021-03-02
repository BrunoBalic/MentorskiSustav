from django.db import models

# Create your models here.

class Enrollments(models.Model):
    student_id = models.ForeignKey(
        'users.Users',
        on_delete=models.CASCADE,
        null=False,
    )
    predmet_id = models.ForeignKey(
        'courses.Courses',
        on_delete=models.CASCADE,
        null=False,
    )
    status = models.CharField(max_length=64, null=False,)

    class Meta:
        verbose_name = "Upis"
        verbose_name_plural = "Upisi"
