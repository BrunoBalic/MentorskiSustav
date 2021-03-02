from django.forms import ModelForm

from .models import Courses


class CourseCreateForm(ModelForm):
    class Meta:
        model = Courses
        fields = [
            'ime',
            'kod',
            'program',
            'bodovi',
            'sem_redovni',
            'sem_izvanredni',
            'izborni',
        ]
