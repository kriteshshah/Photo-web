from django import http
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser, User
from django.http import HttpResponseRedirect, request, Http404
from django.views import View
from django.views.generic import CreateView, UpdateView

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)


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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', 'username',)
    template_name = "profile_update.html"
    success_url = reverse_lazy('web:list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj is None:
            logger.error(f"User with id {self.kwargs.get('pk')} does not exist")
            raise Http404("User does not exist")
        logger.info(f"Retrieved user: {obj.username}")
        return obj
