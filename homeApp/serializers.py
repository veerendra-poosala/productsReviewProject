from rest_framework import serializers
from .models import ImagesModel, UserActionsOnImagesModel

class ImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesModel
        fields = '__all__'

class UserActionsOnImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActionsOnImagesModel
        fields = '__all__'

