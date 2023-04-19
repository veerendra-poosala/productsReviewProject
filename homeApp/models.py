from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ImagesModel(models.Model):
    name = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    image_id = models.AutoField(primary_key=True)
    url = models.URLField(default=None)
    image = models.FileField(default=None, upload_to='images/')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class UserActionsOnImagesModel(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagesModel, on_delete=models.CASCADE, related_name='actions_on_images_url')
    is_accepted = models.BooleanField(default=False)
    action_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} {self.image} {self.is_accepted}"
