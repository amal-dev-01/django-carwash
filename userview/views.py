from django.shortcuts import render,redirect,HttpResponse
from .forms import UserForm
from .models import UserDetails
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import pyotp
from django.core.exceptions import ObjectDoesNotExist
import time
# from django.contrib.auth import login
from django.urls import reverse
from BruteBuster.models import FailedAttempt

# # Create your views here.

# User registeration

def sign_up(request):
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            confirm_password=form.cleaned_data['confirm_password']
            UserData = UserDetails.objects.create_user(first_name=first_name,last_name=last_name ,email=email,phone_number=phone_number,password=password)
            # UserData.is_active=False
            UserData.save()
            # UserData.save()
            # print('no error')
            subject='Car wash'
            totp = pyotp.TOTP(pyotp.random_base32())
            otp = totp.now()
            request.session['otp']=otp
            message=f'Your registeration otp is {otp}'
            recipient=UserData.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
            name='register'
            return redirect('otp', name=name,id=UserData.id)
        else:
            print(form.errors)
            return render(request,'signup.html',{'form':form})
    form=UserForm()
    return render(request,'signup.html',{'form':form}) 

# User login

def loginUser(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            print(email)
            password = request.POST.get('password')
            # print(password)
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                subject = 'Car wash'
                otp_expiration_time = 240
                totp = pyotp.TOTP(pyotp.random_base32(), interval=otp_expiration_time)
                otp = totp.now()

                request.session['otp'] = otp
                message = f'Your login otp is {otp}'
                recipient = user.email
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                name = 'login'
                return redirect('otp', name=name, id=user.id)
            else:
                fails = FailedAttempt.objects.filter(username=email).values()
                f = fails[0]['failures']
                if fails and f < 3:
                    messages.error(request, f'failed attempt {f}')
                elif f >= 3:
                    messages.error(request, 'Your Account is blocked')
                else:
                    messages.error(request, 'Invalid Email or Password')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('login')
    return render(request, 'login.html')


# # home page
# @login_required(login_url='login')
# def home(request):
#     return render(request,'home.html')

# Logout

def logoutUser(request):
    logout(request)
    return redirect('login')

# Otp view

def otpView(request, name,id):
    user =UserDetails.objects.get(pk=id)
    otp = request.session.get('otp')
    print(otp)
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        # print(otp_input)
        # print(name)
        if name == 'register':
            # print('hi')
            if otp == otp_input:
                # Activate the user account
                user.is_active = True
                print(user.is_active)
                print('user',user)
                user.save()
                print('sec',user.is_active)
                messages.success(request, 'Account activated. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('otp')
        elif name == 'login' or name == 'loginwithotp' :
            try:
                if otp == otp_input:
                    print(otp)
                    print(otp_input)
                    login(request,user)
                    messages.success(request, 'OTP verified. Welcome!')
                    return redirect('home')
                else:
                    print(user,'userrrrrrrrrrrrrrrrrrrrrr')
                    
                    messages.error(request, 'Invalid OTP. Please try again.')
                    return redirect('otp',name='login', id=user.id)
            except KeyError:
                    messages.error(request, 'OTP session expired. Please try logging in again.')
                    return redirect('login')
                
                
        # elif name == 'loginwithotp':
        #     if otp == otp_input:
        #         print(otp)
        #         print(otp_input)
        #         user.login_failed = 0
        #         user.save()
        #         messages.success(request, 'OTP verified. Welcome!')
        #         login(request,user)
        #         return redirect('home')
        #     else:
        #         print(user,'nwnn')
        #         user.login_failed += 1
        #         user.save()
        #         messages.error(request, 'Invalid OTP. Please try again.')
        #         return redirect('otp',name='loginwithotp', id=user.id)
        else:
            if otp == otp_input:
                print(otp)
                print(otp_input)
                messages.success(request, 'OTP verified. Welcome!')
                return redirect('restpass',id=user.id)
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('otp')
    return render(request, 'otp.html')

def loginwithotp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserDetails.objects.get(email=email)
        except UserDetails.DoesNotExist:
            user = None
        if user is not None:
            login(request,user)
            subject='Car wash'
            totp = pyotp.TOTP(pyotp.random_base32())
            otp = totp.now()
            request.session['otp']=otp
            message=f'Your login otp is {otp}'
            recipient=user.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
            name='loginwithotp'
            return redirect('otp',name=name,id=user.id)
        else:
            messages.error( request,'Please check username and password.')
    return render(request, 'loginwithotp.html')
    


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserDetails.objects.get(email=email)
        print(email)
        print(user)
        try:
            user = UserDetails.objects.get(email=email)
            subject='Car wash'
            totp = pyotp.TOTP(pyotp.random_base32())
            otp = totp.now()
            request.session['otp']=otp
            message=f'Your forgot password otp is {otp}'
            recipient=user.email
            send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient],fail_silently=False)
            name='forgot'
            return redirect('otp',name=name,id=user.id)
        except UserDetails.DoesNotExist:
            return render(request, 'home.html')
            
    return render(request, 'forgotpass.html')
    
    
def restPassword(request,id):
    user = UserDetails.objects.get(id=id)
    if request.method == 'POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        print(password)
        print(confirm_password)
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        elif len(password)<3:
            raise forms.ValidationError('password must be atleast 5 length long')
        else:
            user.set_password(password)
            user.save()
            return redirect('login')
    return render(request, 'restpass.html')



