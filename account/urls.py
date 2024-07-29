from django.urls import path, reverse_lazy, register_converter

from django.contrib.auth.views import LogoutView

from .views import SignUpView, CustomLoginView, CustomLogout, ProfileUpdateView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(success_url=reverse_lazy('web:list')), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', CustomLogout.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
]
