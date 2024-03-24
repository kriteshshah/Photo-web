import http

from django.urls import path
from django.shortcuts import redirect
from .views import (
    PhotoListView,
    PhotoTagListView,
    PhotoDetailView,
    PhotoCreateView,
    PhotoUpdateView,
    PhotoDeleteView, ToggleLikeView
)

app_name = 'web'

urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),

    path('tag/<slug:tag>/', PhotoTagListView.as_view(), name='tag'),

    path('web/<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('web/create/', PhotoCreateView.as_view(), name='create'),

    path('web/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('web/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

    path('toggle_like/<int:pk>/', ToggleLikeView.as_view(), name='toggle_like'),

]
