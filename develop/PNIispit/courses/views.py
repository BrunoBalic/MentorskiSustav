from django.shortcuts import render, redirect
from django.views.generic.list import View, ListView
from django.views.generic import DetailView, TemplateView, CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from .models import Courses
from .forms import CourseCreateForm
from myauth.mixins import MentorRequiredMixin

# Create your views here.

class CoursesView(LoginRequiredMixin, MentorRequiredMixin, ListView):
    model = Courses
    template_name = 'courses/courses-list.html'


# mislim da ovdje ne koristim CreateView na pravi nacin, treba popraviti
class CourseCreateView(LoginRequiredMixin, MentorRequiredMixin, CreateView):
    template_name = 'courses/course-create.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': CourseCreateForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CourseCreateForm(request.POST)
        if form.is_valid():
            c = form.save()
            c.save()
            return redirect('courses')
        return render(request, self.template_name, {'form': form})


class CourseDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        template_name = 'courses/course-detail.html'

        # predmet = Courses.objects.get(id=3)
        # predmet = Courses.objects.get(id=self.request.GET.get('course_id')) # ne ovako
        predmet = Courses.objects.get(id=kwargs['course_id'])  # ovako
        # naziv key-a u context-u nesmije imati minuse -, zamjeniti ih sa _
        context['course_detail'] = predmet

        return render(request, template_name, context)


# radi
# DetailView mi u context sprema objekt modela pod nazivom 'object'
class CourseDetailView2(LoginRequiredMixin, DetailView):
    model = Courses
    # ako ne navedem ime template-a, po default-u je appname/appname_detail, za DetailView
    template_name = 'courses/course-detail.html'


# radi
# ako nasljedim DetailView onda mi ur url-u moze biti samo <pk> ili <slug>
class CourseDetailView3(LoginRequiredMixin, DetailView):
    model = Courses
    # ako ne navedem ime template-a, po default-u je appname/appname_detail, za DetailView
    template_name = 'courses/course-detail.html'

    # ovdje samo testiram kako dodati jos nesto u context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = self.kwargs['pk']
        context['id_from_url'] = c_id
        return context


# cini mi se da je najbolje nasljediti TemplateView ako mi treba neki obicni view
# tj. ako necu koristiti list, detail...
class CourseDetailView4(LoginRequiredMixin, TemplateView):
    template_name = 'courses/course-detail.html'

    # get_context_data moram override da bi dohvatio parametar iz URL-a
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['id_from_url'] = self.kwargs['course_id']
        predmet = Courses.objects.get(id=self.kwargs['course_id'])  # moram navest self.kwargs
        context['course_detail'] = predmet
        return context


class CourseEditView(LoginRequiredMixin, MentorRequiredMixin, UpdateView):
    model = Courses
    template_name = 'courses/course-edit.html'
    fields = [
        'ime',
        'kod',
        'bodovi',
        'sem_redovni',
        'sem_izvanredni',
        'izborni',
        'program',
    ]
    success_url = '/courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['id_from_url'] = self.kwargs['course_id']
        context['id_from_url'] = self.kwargs['pk']
        return context
