from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser
from django.contrib import messages
from .Emailbackend import EmailBackend
from django.contrib.auth import login,logout,authenticate
from uuid import uuid4 
from django.core.mail import send_mail
from LMS_Web import settings
from django.contrib.auth.decorators import login_required


def send_email_after_registration(email,token):
    subject=f"Account need verification"
    message=f"your account needs to be verified. please click this link http://127.0.0.1:8000/accounts/verify/{token}"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    
def send_forgot_password_link(email,token):
    subject=f"Forgot your password ?"
    message=f"please click this link to reset your password, if done please ignore. http://127.0.0.1:8000/accounts/reset_password/{token}"
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

def registration_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,"Email already exist")
            return HttpResponseRedirect(reverse('registration'))
        
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,"username already exist")
            return HttpResponseRedirect(reverse('registration'))
        
        user=CustomUser.objects.create_user(username=username,email=email,token=str(uuid4()),password=password)
        user.save()
        
        send_email_after_registration(email,user.token)
        
        messages.success(request,"user created !")
        return HttpResponseRedirect(reverse('registration'))
    return render(request,"accounts/registration.html")


def login_view(request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,password)
        user=EmailBackend.authenticate(request,username=email,password=password)
        print("user is ",user)
        if user:
            if user.is_verified:
                login(request,user=user,backend='accounts.Emailbackend.EmailBackend')
                messages.success(request,"user logged in !")
                return HttpResponseRedirect(reverse("home_view"))
            else:
                messages.error(request,"user is not verified. please check your mail")
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request,"Invalid user !")
    return render(request,"accounts/login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"you are logged out now !")
    return HttpResponseRedirect(reverse("login"))


def verify_usermail(request,authtoken):
    try:
        user_obj=CustomUser.objects.filter(token=authtoken).first()
        if user_obj:
            user_obj.is_verified=True
            user_obj.save()
            messages.success(request,"Email verified successfully ! please login now .")
            return HttpResponseRedirect(reverse("login"))
    except Exception as e:
        print(e)
        messages.error(request,"Email not verified.")
        return HttpResponseRedirect(reverse("login"))
    
def forgot_password(request):
    if request.method=='POST':
        email=request.POST.get("email")
        user_obj=CustomUser.objects.filter(email=email).first()
        if user_obj:
            user_obj.token=str(uuid4())
            user_obj.save()
            send_forgot_password_link(email,user_obj.token)
            messages.success(request,"password reset link has been sent , please check your email.")
        else:
            messages.error(request,"Account does not exists with this email id !")
    return render(request,"accounts/forgot_password.html")

def verify_password_reset_link(request,token):
    user_obj=CustomUser.objects.filter(token=token).first()
    if user_obj:
        if request.method=='POST':
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            
            if password1!=password2:
                messages.error(request,"password not matched. please do it carefully")
            elif len(password1) < 6:
                messages.error(request,"password length must be 6 digit at least")
            else:
                user_obj.set_password(password1)
                user_obj.token=str(uuid4())
                user_obj.save()
                messages.success(request,"password has been changed uccessfully. please login now !")    
                return HttpResponseRedirect(reverse("login"))        
            return render(request,"accounts/password_reset.html")
        else:
            return render(request,"accounts/password_reset.html")
    else:
        return render(request,"accounts/reset_error.html")
    

@login_required(login_url='/accounts/login/')  
def update_profile(request):
    user=request.user
    if request.method=='POST':
        user_id=request.user.id
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        
        try:
            user_obj=CustomUser.objects.get(id=user_id)
            user_obj.first_name=first_name
            user_obj.last_name=last_name
            user_obj.email=email
            user_obj.username=username
            
            if password1 != None and password1 !="":
                if len(password1)< 6:
                    messages.error(request,"password length must be 6 digit or above")
                    raise Exception
                elif password1 != password2:
                    messages.error(request,"new password and confirm password not matched !")
                    raise Exception
                else:
                    user_obj.set_password(password1)
            user_obj.save()
            messages.success(request,"your profile got updated")
            return HttpResponseRedirect(reverse("account_profile"))
        except Exception as e:
            print(e)
            
    return render(request,"accounts/account_profile.html",{'user':user})
    
        