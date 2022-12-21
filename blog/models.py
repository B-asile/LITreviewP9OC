from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from LITreview.settings import AUTH_USER_MODEL
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,
                              upload_to='mediaLitReview')
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (300, 300)

    def resize_image(self):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(self.IMAGE_MAX_SIZE)
            image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class UserFollows(models.Model):
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_following')
    followed_user = models.ForeignKey(to=AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    class Meta():
        unique_together=('user', 'followed_user')


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=
                                              [MinValueValidator(0),
                                               MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def range_rating(self):
        return range(self.rating)
