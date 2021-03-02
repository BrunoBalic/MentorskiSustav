from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import FormView

from .forms import MyAuthenticationForm
from .mixins import LogoutRequiredMixin

# Create your views here.

def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("register1")

    if request.POST:
        form = MyAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("register1")
    else:
        form = MyAuthenticationForm()

    # 'login_form' je ime u dictionary-u, preko tog imena pristupim formi u html template-u
    context['login_form'] = form

    template = loader.get_template('myauth/login.html')

    return render(request, 'myauth/login.html', context)
    # return HttpResponse(template.render(context, request))


def logout_view(request):
    logout(request)
    return redirect('login1')

# kada koristim CBV onda mi se u centext sprema forma form_class, pod nazivom 'form'
class LoginView(LogoutRequiredMixin, FormView):
    form_class = MyAuthenticationForm
    template_name = 'myauth/login.html'
    success_url = '/upisni-list'

    def form_valid(self, form):
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(self.request, user)
                return super().form_valid(form)

    extra_context = {
        'login_form': MyAuthenticationForm()
    }

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
