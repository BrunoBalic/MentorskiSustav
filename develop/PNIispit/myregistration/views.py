from django.views.generic.edit import FormView

from .forms import MyUserCreationForm
from myauth.mixins import LogoutRequiredMixin

# Create your views here.

class RegisterView(LogoutRequiredMixin, FormView):
    form_class = MyUserCreationForm
    template_name = 'myregistration/register.html'
    success_url = '/upisni-list'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
