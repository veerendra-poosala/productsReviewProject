from django.urls import path
from .views import *

urlpatterns = [
    
    path('list/',GetImagesView.as_view(),name='listImages'),
    path('update/<str:user_input>/',PerformOperationsOnImageView.as_view(),name='update'),
    path('get_csrf_token/',generate_csrf_token,name='get_csrf_token'),
    path('history/',GetHistoryOfImages.as_view(),name='history')
]
