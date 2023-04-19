from django.contrib import admin
from .models import ImagesModel,UserActionsOnImagesModel
# Register your models here.

admin.site.register(ImagesModel)
admin.site.register(UserActionsOnImagesModel)