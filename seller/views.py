from secrets import choice
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail
from seller.models import Seller

# Create your views here.

def index3(request):
    try:
            uid = Seller.objects.get(Email=request.session['email'])
            return render(request,'index3.html',{'uid':uid})
    except:
            return render(request,'login.html',{'msg':'Session has Expired.'})
    

def login(request):
     if request.method == 'POST':
          try:
            uid = Seller.objects.get(Email=request.POST['email'])
            if request.POST['password'] == uid.password:
               request.session['email'] = request.POST['email']
               return render(request,'index3.html',{'uid': uid})
            return render(request,'login.html',{'msg':'Password is Incorrect.'})
          except:
               return render(request,'login.html',{'msg':'Account Does not Exists.'})
     return render(request,'login.html')

def sign_up1(request):
    if request.method == "POST":
          try:
               Seller.objects.get(Email=request.POST['email'])
               msg = "Email Already Exist."
               return render(request,'sign-up1.html',{'msg':msg})
          except:
               if request.POST['password'] == request.POST['cpassword']:
                    otp = randrange(1000,9000)
                    subject = 'OTP verification'
                    message = f'Your OTP is {otp}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'], ]
                    send_mail( subject, message, email_from, recipient_list )
                    global temp 
                    temp = {
                         'fname' : request.POST['fname'],
                         'lname' : request.POST['lname'],
                         'email' : request.POST['email'],
                         'mobile' : request.POST['mobile'],
                         'password' : request.POST['password'],
                    }
                    return render(request,'otp1.html',{'msg':'OTP sent on your Email !!!.','otp':otp})
               return render(request,'sign-up1.html',{'msg':'Both Passwords Are not Same.'})
    return render(request,'sign-up1.html')

def otp1(request):
     if request.POST['uotp'] == request.POST['otp']:
          global temp
          Seller.objects.create(
               fname = temp['fname'],
               lname = temp['lname'],
               Email = temp['email'],
               mobile = temp['mobile'],
               password = temp['password'],

          )
          del temp
          return render(request,'login.html',{'msg':'Account Created'})
     return render(request,'otp1.html',{'msg':'Invalid OTP','otp':request.POST['otp']})

def forgot_password1(request):
     if request.method == 'POST':
          try:
               uid = Seller.objects.get(Email=request.POST['email'])
               s='qwertyiopuasdfghjklzxcvbnm@123456789'
               password = ''.join(choices(s,k=8))
               subject = 'Password Has been Reset.'
               message = f'Your new Password is {password}'
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [request.POST['email'], ]
               send_mail(subject, message, email_from, recipient_list )
               uid.password = password
               uid.save()
               return render(request,'login.html',{'msg':'New password sent on your Email.'})
          except:
               return render(request,'sign-up1.html',{'msg':'Account Does not Exists.'})
     return render(request,'forgot-password1.html')

def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request,'index3.html')   
    except:
        return render(request,'index3.html',{'msg':'Session Expired'})   

def product(request):
     # uid = Seller.objects.get(Email=request.session['email'])
     uid = Seller.objects.get(Email=request.session['email'])    
     if request.method == 'POST':
          
          Product.objects.create(
               product_owner = uid,
               product_name = request.POST['name'],
               product_description = request.POST['message'],
               product_pic = request.FILES['image'],
               product_price = request.POST['price'],
               quantity = request.POST['Quantity'],
          )
          msg = 'Product Added Successfully.' 
          return render(request,'product.html',{'uid':uid,'msg':msg})
     return render(request,'product.html',{'uid':uid})

def view(request):
     uid = Seller.objects.get(Email=request.session['email'])
     products = Product.objects.filter(product_owner=uid)
     print(products)
     return render(request,'view.html',{'uid':uid,'products':products})                

#def delete_service(request,pk):
#    uid = User.objects.get(email=request.session['email'])
#    service = Service.objects.get(id=pk)
#    service.delete()
#    return redirect('my-service')


def delete_product(request,pk):
     uid = Seller.objects.get(Email=request.session['email'])
     products = Product.objects.get(id=pk)
     products.delete()
     return redirect('view')

#def edit_service(request,pk):
#    uid = User.objects.get(email=request.session['email'])
#    service = Service.objects.get(id=pk)
#    if request.method == 'POST':
#        service.name = request.POST['sname']
#        service.sector = request.POST['sector']
#        service.min_charge= request.POST['charge']
#        service.area = request.POST['area']
#        service.des = request.POST['des']
#        service.save()
#        return redirect('my-service')
#    return render(request,'edit-service.html',{'uid': uid,'service':service})



def edit_product(request,pk):
     uid = Seller.objects.get(Email=request.session['email'])
     products = Product.objects.get(id=pk)
     if request.method == 'POST':
         products.product_name = request.POST['name']
         products.product_description = request.POST['message']
         products.product_price = request.POST['price']
         products.quantity = request.POST['Quantity']
         if 'product_pic' in request.FILES:
          products.product_pic = request.FILES['image']
         products.save()
         return redirect('view')
     return render(request,'edit-product.html',{'uid':uid,'products':products})

