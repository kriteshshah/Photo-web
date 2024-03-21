from django import http
from django.conf import settings
from django.http import HttpResponseRedirect, request
from django.views import View
from django.views.generic import CreateView

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy


class SignUpView(CreateView):
    template_name = 'signup.html'
    parameter = True
    form_class = UserCreationForm

    success_url = reverse_lazy('web:list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)

        return to_return


class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('account:login'))
