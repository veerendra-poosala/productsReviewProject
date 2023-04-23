

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
        userid = request.user.id
        #print('username',userid)
        user = User.objects.get(pk=userid)
        username=user.first_name
        is_accepted = request.data['is_accepted']


        data = {
            'username': userid,
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
                message = f'Hey {username} you Selected the {image.name} image'
                j_data = {
                    'message': message,
                    'status': 200
                }
                json_data = json.dumps(j_data)
            else:
                message = f'Hey {username} you Rejected the {image.name} image'
                j_data = {
                    'message': message,
                    'status': 200
                }
            json_data = json.dumps(j_data)
            
            
            return HttpResponse(json_data,content_type='application/json')
        else:
            print(serializer.errors)
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

        send_data = []

        for data in serializer.data:

            #print(data['is_accepted'])
            #print(type(data['username']),data['username'])

            
            username = User.objects.get(pk=data['username'])
            #print(username.first_name)

            image = ImagesModel.objects.get(pk=data['image'])
            #print(image.name)

            user_actions_model_obj = UserActionsOnImagesModel.objects.get(pk=data['id'])
            is_accepted = user_actions_model_obj.is_accepted
            #print(is_accepted)

            action_datetime = user_actions_model_obj.action_datetime
            time = action_datetime.strftime("%d %b %Y %I:%M %p")
            #print(time)
            #print(action_datetime)
            
            
            data_obj = {
                'username':username.first_name,
                'image':image.name,
                'is_accepted':is_accepted,
                'action_datetime':time

            }
            #print(data_obj) 
            j_data = json.dumps(data_obj)
            #print(j_data)
            send_data.append(data_obj)
            
        send_data = json.dumps(send_data)   
        x_data = {
            'message':send_data,
            'status_code':200

        }
        
        x_data = json.dumps(x_data)
        #json_data = JSONRenderer().render(x_data)
        #print(type(json_data),json_data)
        #print(type(send_data),send_data)
        #print(type(json_data),json_data)
        #return render(request,'history.html',{'data':x_data})

        #next emcheyali ante get method raasukovatame , template loki velli
        return HttpResponse(send_data,content_type='application/json')

    
