from django.db import models

from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


class Photo(models.Model):
    title = models.CharField(max_length=45)

    description = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    submitter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    tags = TaggableManager()

    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Like(models.Model):
    photo = models.ForeignKey(Photo, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='liked_photos', on_delete=models.CASCADE)
    like = models.BooleanField(default=True)  # True for like, False for dislike

    class Meta:
        unique_together = ['photo', 'user']