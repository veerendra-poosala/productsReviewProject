

from django.shortcuts import render,redirect
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import APIView

from django.http import JsonResponse,HttpResponse

from .models import *
from .serializers import *

from django.contrib.auth.decorators import login_required


from regApp.views import nav_to_login_page

from django.middleware.csrf import get_token

from datetime import datetime

import json


from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


#generating csrf token
def generate_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})
    


class GetImagesView(APIView):
    serializer_class = ImagesModelSerializer


    def get(self, request):
        try:
            if request.user.is_authenticated:
                # Retrieve all images
                images = ImagesModel.objects.all()

                # Serialize the images
                serializer = self.serializer_class(images, many=True)

                serialized_images = JSONRenderer().render(serializer.data)
           
                # Return the serialized images as a response
                return HttpResponse(serialized_images,content_type='application/json')
            else:
                #send error 
                return redirect('nav_to_login_page')
        except:
            print('something went wrong')

class PerformOperationsOnImageView(APIView):
    
    serializer_class = UserActionsOnImagesModel

    def post(self, request,user_input):

        image = ImagesModel.objects.get(pk=int(user_input)).image_id
        username = request.user.id
        is_accepted = request.data['is_accepted']


        data = {
            'username': username,
            'image': image,
            'is_accepted': is_accepted, # use the value of is_accepted variable
            
        }
        
        serializer = UserActionsOnImagesModelSerializer(data=data)
        

        
        if serializer.is_valid():
            image_id = serializer.validated_data['image'].image_id
            is_accepted = serializer.validated_data['is_accepted']
            user_action = 'accept' if is_accepted else 'reject'
            image = ImagesModel.objects.get(pk=image_id)
            UserActionsOnImagesModel.objects.create(username=request.user, image=image, is_accepted=is_accepted)
            image.is_accepted = is_accepted
            image.save()

            if is_accepted:
                message = f'Hey {request.user} you Selected the {image.name} image'
                j_data = {
                    'message': message,
                    'status': 200
                }
                json_data = json.dumps(j_data)
            else:
                message = f'Hey {request.user} you Rejected the {image.name} image'
                j_data = {
                    'message': message,
                    'status': 200
                }
            json_data = json.dumps(j_data)
            
            
            return HttpResponse(json_data,content_type='application/json')
        else:
            #print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class GetHistoryOfImages(APIView):    

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserActionsOnImagesModelSerializer
    
    def get(self, request):
        user_id = self.request.user.id
        queryset = UserActionsOnImagesModel.objects.filter(username_id=user_id)
        serializer = self.serializer_class(queryset, many=True)

        
        data = serializer.data
        return render(request,'history.html',{'data':data})


    
