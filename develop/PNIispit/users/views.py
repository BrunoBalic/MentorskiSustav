from django.shortcuts import render
from django.views.generic.list import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Users
from myauth.mixins import MentorRequiredMixin

# Create your views here.

class AllUsersView(LoginRequiredMixin, MentorRequiredMixin, ListView):
    model = Users
    template_name = 'users/students-list.html'

class StudentsView(LoginRequiredMixin, MentorRequiredMixin, View):
    def get(self, request):
        context = {}
        template_name = 'users/students-list.html'

        students_all = Users.objects.filter(user_role='STUDENT')
        context['object_list'] = students_all

        return render(request, template_name, context)
