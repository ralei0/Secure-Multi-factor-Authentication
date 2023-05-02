from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import uuid
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from user.models import *
import random


def home(request):
    return render(request,'main/main-home.html')

def about(request):
    return render(request,'main/main-about.html')

def contact(request):
    return render(request,'main/main-contact.html')


def user_login(request):
    # user = request.user
    # if user.is_authenticated:
    #     return redirect("base")
                
		        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password,'pssword')
        user = authenticate(request=None,email=email, password=password)
        print(user,'user')
        if user is not None:
            if user.gpa_status == False:
                messages.info(request,'Graphical Password Location Pending')
                return redirect('gpi_register')
            login(request,user)
            gen_otp = random.randint(1000, 9999)
            print(gen_otp,'otp')
            o = otp_m.objects.create(otp_set=gen_otp)
            o_id = o.pk
            mail_message = f'Hey Your otp is {gen_otp}'
            user_email = user.email
            send_mail('otp verification',mail_message,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
        

            messages.success(request,'Otp sent Successfull')
            return redirect('send_otp',o_id)

        else:
            print('invalid')
            messages.error(request,'Invalid Credentials')
            return redirect('user_login')
    return render(request,'main/main-userlogin.html')

def _send_otpp(request,o_id):
    o = otp_m.objects.get(pk = o_id)
    gen_otp = o.otp_set
    print(o.otp_set,'userrrrrrrrrr')
    if otp:=request.POST.get('otp'):
        otp = int(otp)
        # otp_validation(gen_otp,otp)
        return redirect('otp_validation',gen_otp,otp,o_id)    
    return render(request,'user/user-otp.html')



def otp_validation(request,gen_otp,otp,o_id):
    print(gen_otp,type(gen_otp),'gen')
    print(otp,type(otp),'uotp')
    if gen_otp == otp:
        print('success')
        messages.success(request,'OTP Verified successfully')

        return redirect('gpi_login')
    else:
        print('wrong')
        messages.error(request,'Invalid OTP')
        return redirect('send_otp',o_id)






    

def user_register(request):
    try:
        if request.method == 'POST':
            # _extracted_from_user_register_4(request)
            fullname=request.POST.get('fullname')
            email=request.POST.get('email')
            contact=request.POST.get('contact')
            city=request.POST.get('city')
            pic=request.FILES['pic']
            gpa=request.FILES['gpa']
            print(gpa,'gpaimg')
            password=request.POST.get('password')
            print(fullname,email,contact,city,pic,password)
            user = MyUser.objects.create_user(email, password)
            ids = user.id
            request.session["gpi_id"]=ids
            user.fullname = fullname
            user.contact = contact
            user.city = city
            user.image = pic
            user.gpa = gpa
            user.save()
            ftoken = str(uuid.uuid4())
            Profile.objects.create(user=user,forget_token=ftoken)
            messages.success(request,'Registration Successfull')
            return redirect('gpi_register')

    except IntegrityError:
        messages.warning(request,'Email Has Already Been Taken')
        return redirect('user_register')
    return render(request,'main/main-user-register.html')


# # TODO Rename this here and in `user_register`
# def _extracted_from_user_register_4(request):
#     fullname=request.POST.get('fullname')
#     email=request.POST.get('email')
#     contact=request.POST.get('contact')
#     city=request.POST.get('city')
#     pic=request.FILES['pic']
#     gpa=request.FILES['gpa']
#     password=request.POST.get('password')
#     print(fullname,email,contact,city,pic,password)
#     user = MyUser.objects.create_user(email, password)
#     # id = user.pk
#     # request.session["gpi_id"]=request.user
#     user.fullname = fullname
#     user.contact = contact
#     user.city = city
#     user.image = pic
#     user.gpa = gpa
#     user.save()
#     ftoken = str(uuid.uuid4())
#     Profile.objects.create(user=user,forget_token=ftoken)


def gpi_register(request):
  
    try:    
        userp=MyUser.objects.get(email=request.user)
    except:
        userpass=request.session['gpi_id']
        userp=MyUser.objects.get(id=userpass)
    print(userp,'serrrrr')
    print(userp.image,'image')

    if request.method == "POST":
        point1=request.POST.get("point1")
        point2=request.POST.get("point2")
        point3=request.POST.get("point3")
        point4=request.POST.get("point4")
        userp.point1=point1
        userp.point2=point2
        userp.point3=point3
        userp.point4=point4
        userp.gpa_status = True
        userp.save()
        messages.success(request,'locations Registered successfully')
        return redirect('user_login')
    con = {"i":userp}
    return render(request, 'main/user-register-gpi.html',con)





def gpi_update(request):
    try:    
        userp=MyUser.objects.get(email=request.user)
    except:
        userpass=request.session['gpi_id']
        userp=MyUser.objects.get(id=userpass)
    print(userp,'serrrrr')
    if request.method == "POST":
        point1=request.POST.get("point1")
        point2=request.POST.get("point2")
        point3=request.POST.get("point3")
        point4=request.POST.get("point4")
        userp.point1=point1
        userp.point2=point2
        userp.point3=point3
        userp.point4=point4
        userp.save()
        messages.success(request,'locations updated successfully')
        return redirect('myprofile')
    con = {"i":userp}
    return render(request, 'user/user-update-gpi.html',con)




def gpi_login(request):
    user_det=MyUser.objects.get(email=request.user)
    print(user_det.image,'image')
    if request.method == "POST":
        point1=request.POST.get("point1")
        point2=request.POST.get("point2")
        point3=request.POST.get("point3")
        point4=request.POST.get("point4")
        x1=point1.split(",")
        y1=[]
        for i in x1:
            y1.append(int(i))
        print(y1)
        x2=point2.split(",")
        y2=[]
        for i in x2:
            y2.append(int(i))
        print(y2)
        x3=point3.split(",")
        y3=[]
        for i in x3:
            y3.append(int(i))
        print(y3)
        x4=point4.split(",")
        y4=[]
        for i in x4:
            y4.append(int(i))
        print(y4)
        z1=user_det.point1.split(",")
        a1=[]
        for i in z1:
            a1.append(int(i))
        print(a1)
        z2=user_det.point2.split(",")
        a2=[]
        for i in z2:
            a2.append(int(i))
        print(a2)
        z3=user_det.point3.split(",")
        a3=[]
        for i in z3:
            a3.append(int(i))
        print(a3)
        z4=user_det.point4.split(",")
        a4=[]
        for i in z4:
            a4.append(int(i))
        print(a4)
        if (((y1[0]-10 <= a1[0]) and (a1[0] <= y1[0]+10)) and ((y1[1]-10 <= a1[1]) and (a1[1] <= y1[1]+10))) and (((y2[0]-10 <= a2[0]) and (a2[0] <= y2[0]+10)) and ((y2[1]-10 <= a2[1]) and (a2[1] <= y2[1]+10))) and (((y3[0]-10 <= a3[0]) and (a3[0] <= y3[0]+10)) and ((y3[1]-10 <= a3[1]) and (a3[1] <= y3[1]+10))) and (((y4[0]-10 <= a4[0]) and (a4[0] <= y4[0]+10)) and ((y4[1]-10 <= a4[1]) and (a4[1] <= y4[1]+10))):
            messages.success(request,'Logged in successfully')
            return redirect('base')
        # print(point1,point2,point3,point4)
        # if user_det.point1 == point1 and user_det.point2 == point2 and user_det.point3 == point3 and user_det.point4 == point4:
        #     return redirect('user_dashboard')
        else:
            messages.error(request,'Incorrect Locations')
            return redirect('gpi_login')
    context={"x":user_det}
    return render(request,'main/user-login-gpi.html',context)





















def forget_password(request):  # sourcery skip: do-not-use-bare-except, extract-method
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = MyUser.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            user_email = user.email
            print(user_email)
            ftoken = profile.forget_token
            mail_message = f'Hey Your Reset Password Link is http://127.0.0.1:8000/reset-password/{ftoken}/'
            print(mail_message)
            send_mail('Password Reset Request',mail_message,settings.EMAIL_HOST_USER,[user_email],fail_silently=False)
            messages.info(request,'MAIL SEND')
    except:
        messages.warning(request,"Email Does not Exist")

    return render(request,'main/main-forgot-password.html')

def log_out(request):
    logout(request)
    messages.info(request,'Logout Successfull')
    
    return redirect('user_login')


def reset_password(request,id):
    if request.method == 'POST':
        password = request.POST['password']
        profile = Profile.objects.get(forget_token=id).user
        print(profile,'profile')
        user = MyUser.objects.get(email=profile)
        user.set_password(password)
        user.save()
        messages.info(request,'Password Changed Please Login! ')
        return redirect('user_login')
    return render(request,'main/main-reset-password.html')


@login_required(login_url='user_login')
def base(request):  
    user = MyUser.objects.get(email = request.user)
    return render(request,'user/user-base.html')

@login_required(login_url='user_login')
def myprofile(request):
    user = MyUser.objects.get(email = request.user)
    if request.method == 'POST':
        fullname = request.POST.get("fullname")
        contact = request.POST.get("contact")
        city = request.POST.get("city")
        print(city)
        state = request.POST.get("state")
        print(fullname,'hiii')
        user.fullname = fullname
        user.contact = contact
        user.city = city
        user.save()
        if len(request.FILES) != 0:
            image = request.FILES["pic"]
            user.image = image
            user.save()
        messages.success(request,'Updated Successfully')
        return redirect('myprofile')
    context = {'user':user}
    return render(request,'user/user-myprofile.html',context)

@login_required(login_url='user_login')
def change_password(request):
    user = MyUser.objects.get(email = request.user)
    user_pass = user.password
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        if check_password(old_password,user.password):
            if new_password1 == new_password2:
                user.set_password(new_password2)
                us = user.save()
                update_session_auth_hash(request,user)
                print('password changed')
                messages.success(request,'Password Updated Successfully')
                return redirect('myprofile')
            else:
                messages.warning(request,'New password and Confirm New password Should be same')

                print('New password and Confirm New password Should be same')
        else:
            messages.warning(request,'Enter your correct old password')
            print('Enter your correct old password')
    return render(request,'user/user-change-password.html')

