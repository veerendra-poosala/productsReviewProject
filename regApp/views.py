


from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from phonenumbers import parse, is_valid_number
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import get_user_model

from django.db.utils import IntegrityError

from rest_framework.renderers import JSONRenderer

def home(request):
    if request.user.is_authenticated:
        
        return render(request, 'home.html')
    else:
        return render(request,'login.html')

def nav_to_register_page(request):
    return render(request,'signup.html')

def nav_to_login_page(request):
    
    return render(request,'login.html')

def nav_to_otp_page(request):
    return render(request,'verify_otp.html')



#validating phone number
def clean_phone_number(phone_number):
    
    parsed_number = parse(phone_number, 'IN')
    if not is_valid_number(parsed_number):
        return False
        #raise ValidationError("Invalid phone number")
    return True

def send_otp(phone_number):
        
        otp = get_random_string(length=6, allowed_chars='1234567890')
        '''
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        otp = get_random_string(length=6, allowed_chars='1234567890')
        message = client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=f"Your OTP is: {otp}"
        )
        '''
        return otp

def verify_otp(request):
    if request.method == 'POST':
        otp_number = request.POST['otp_number']
        is_valid_number = len(otp_number) == 6
        
        if is_valid_number and otp_number == '000000':

            return redirect('home')
        else:
            auth.logout(request)
            return redirect('nav_to_register_page')
        
        
    else:
        
        return redirect('nav_to_register_page')

def signup_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        is_valid_number = clean_phone_number(phone_number)
        form_data = request.POST 
        

        if is_valid_number:


            username = request.POST['username']
            
            if username.strip() != '':
                #user_obj = CustomUser
                #User = get_user_model()
                try:
                    user=User.objects.get(username = request.POST['phone_number'])
                    auth.login(request,user)
                    #sending otp to phone number
                    otp = send_otp(phone_number)
                    #print('otp: ',otp)
                    return redirect('nav_to_otp_page')
                
                except user.DoesNotExist:
                    new_user = User.objects.create_user(username=phone_number,email='xyz@gmail.com',
                                            password='000000',first_name=username, is_staff = False)
                    
                    #sending otp to phone number
                    
                    otp = send_otp(phone_number)

                    auth.login(request,new_user)
                    #print('otp: ',otp)
                    return redirect('nav_to_otp_page')
                except IntegrityError as error:
                    print(f"duplicate key value violates unique constraint : {error}")
                except :
                    pass
            else:
                return redirect('nav_to_register_page')

        else:
            return redirect('nav_to_register_page')
        
        
    else:
        
        return redirect('nav_to_register_page')

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        is_valid_number = clean_phone_number(phone_number)

        if is_valid_number:


            username = request.POST['username']
            
            if username.strip() != '':
                #user_obj = CustomUser
                #User = get_user_model()
                try:
                    user = auth.authenticate(username = phone_number,password = '000000')
                    if user is not None:
                        otp = send_otp(phone_number)
                        #print('otp: ',otp)
                        auth.login(request,user)
                        
                        return redirect('nav_to_otp_page')
                    else:
                        return redirect('nav_to_register_page')
                except IntegrityError as error:
                    print(f"duplicate key value violates unique constraint : {error}")
                except :
                    print('Some thing went wrong')
            else:
                return redirect('nav_to_login_page')

        else:
            return redirect('nav_to_login_page')
        
        
    else:
        
        return redirect('nav_to_login_page')

def logout_view(request):
    auth.logout(request)
    return redirect('nav_to_login_page')
