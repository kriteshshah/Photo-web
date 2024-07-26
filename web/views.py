from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy, reverse

from .models import Photo, Like


class PhotoListView(ListView):
    model = Photo

    template_name = 'list.html'

    context_object_name = 'photos'


class PhotoTagListView(PhotoListView):
    template_name = 'taglist.html'

    # Custom function
    def get_tag(self):
        return self.kwargs.get('tag')

    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'detail.html'
    context_object_name = 'photo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            like_status = photo.likes.filter(user=user).first()
            context['like_status'] = like_status.like if like_status else None

        context['like_count'] = photo.likes.filter(like=True).count()
        context['dislike_count'] = photo.likes.filter(like=False).count()

        return context


class ToggleLikeView(View):
    def post(self, request, pk):
        if request.user.is_authenticated:
            photo = get_object_or_404(Photo, pk=pk)
            user = request.user

            like_instance, created = Like.objects.get_or_create(photo=photo, user=user)

            if 'like' in request.POST:
                if like_instance.like:
                    like_instance.like = False
                    if photo.likes_count != 0:
                        photo.likes_count -= 1
                else:
                    if like_instance.dislike:
                        like_instance.dislike = False
                        if photo.dislikes_count != 0:
                            photo.dislikes_count -= 1
                    like_instance.like = True
                    photo.likes_count += 1

            elif 'dislike' in request.POST:
                if like_instance.dislike:
                    like_instance.dislike = False
                    if photo.dislikes_count != 0:
                        photo.dislikes_count -= 1
                else:
                    if like_instance.like:
                        like_instance.like = False
                        if photo.likes_count != 0:
                            photo.likes_count -= 1
                    like_instance.dislike = True
                    photo.dislikes_count += 1

            like_instance.save()
            photo.save()

            return JsonResponse({'like_count': photo.likes_count, 'dislike_count': photo.dislikes_count})
        return JsonResponse({'error': 'You must be logged in to like or dislike'}, status=401)


class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo

    fields = ['title', 'description', 'image', 'tags']

    template_name = 'create.html'
    success_url = reverse_lazy('web:list')

    def form_valid(self, form):
        form.instance.submitter = self.request.user

        return super().form_valid(form)

    def myview(self, request):
        return HttpResponseRedirect('account:login', request)


class UserIsSubmitter(UserPassesTestMixin):

    # Custom method
    def get_photo(self):
        return get_object_or_404(Photo, pk=self.kwargs.get('pk'))

    def test_func(self):

        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied('Sorry you are not allowed here')


class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'update.html'

    model = Photo

    fields = ['title', 'description', 'image', 'tags']

    success_url = reverse_lazy('web:list')


class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'delete.html'

    model = Photo

    success_url = reverse_lazy('web:list')
