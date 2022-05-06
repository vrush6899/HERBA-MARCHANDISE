from django.shortcuts import redirect, render
from django.http import *
from seller.models import Product as p
from .models import *
from random import randrange, choices
from seller import models as sm
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.
def index(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        products = sm.Product.objects.all()[::-1]
        print(products)
        return render(request,'index.html',{'uid':uid,'products':products})
    except:
        products = sm.Product.objects.all()[::-1]
        return render(request,'index.html',{'products':products})    



def sign_in(request):
    if request.method == 'POST':
        try:
            uid = User.objects.get(email=request.POST['email'])
            products = sm.Product.objects.all()[::-1]
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return render(request,'index.html',{'uid':uid,'products':products})
            return render(request,'sign-in.html',{'msg':'Password is Incorrect.'})
        except:
            return render(request,'sign-in.html',{'msg':'Account Does not Exists.'})
    return render(request,'sign-in.html')
    

def sign_up(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg = 'email already exists.'
            return render(request,'sign-up.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpass']:
                otp = randrange(1000,9999)
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
                         'password' : request.POST['password'],
                         'mobile' : request.POST['mobile'],
                    }
                return render(request,'otp.html',{'msg':'OTP sent on your Email !!!.','otp':otp})
            return render(request,'sign-up.html',{'msg':'Both Passwords are not Same.'})
    return render(request,'sign-up.html')

  


def otp(request):
    if request.POST['uotp'] == request.POST['otp']:
        global temp
        User.objects.create(
            fname = temp['fname'],
            lname = temp['lname'],
            email = temp['email'],
            mobile = temp['mobile'],
            password = temp['password'],
        )
        del temp
        return render(request,'sign-in.html',{'msg':'Account Created !!!'})
    return render(request,'otp.html',{'msg':'Invalid OTP','otp':request.POST['otp']})
    
def log_out(request):
    try:
        products = sm.Product.objects.all()[::-1]
        request.session['email']
        del request.session['email']
        return render(request,'index.html',{'products':products})   
    except:
        return render(request,'index.html',{'msg':'Session Expired','products':products})   

def blog(request):
    return render(request,'blog.html')

def cart(request):
    uid = User.objects.get(email=request.session['email'])
    try:
        cart = Cart.objects.get(uid=uid)
        return render(request,'cart.html',{'uid':uid,'cart':cart})
    except:
        return render(request,'cart.html',{'uid':uid})

def category(request):
    try:
        uid = User.objects.get(email=request.session['email'])
        products = sm.Product.objects.all()[::-1]
        print(products)
        return render(request,'category.html',{'uid':uid,'products':products})
    except:
        products = sm.Product.objects.all()[::-1]
        return render(request,'index.html',{'products':products})

def checkout(request):
    return render(request,'checkout.html')

def confirmation(request):
    return render(request,'confirmation.html')

def contact(request):
    uid = User.objects.get(email=request.session['email'])
    return render(request,'contact.html',{'uid':uid})

def edit_profile(request):
    uid = User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']
        uid.save()
        return render(request,'index1.html',{'uid':uid,'msg':'Your profile Has been Updated Successfully'})
    return render(request,'edit-profile.html',{'uid':uid})

def single_blog(request):
    return render(request,'single-blog.html')

def single_product(request):
    return render(request,'single-product.html')

def tracking(request):
    uid = User.objects.get(email=request.session['email'])
    return render(request,'tracking.html',{'uid':uid})

def forgot_password(request):
    if request.method == 'POST':
          try:
               uid = User.objects.get(email=request.POST['email'])
               s='qwertyiopuasdfghjklzxcvbnm@123456789'
               password = ''.join(choices(s,k=8))
               subject = 'Password Has Been Reset.'
               message = f'Your New Password is {password}'
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [request.POST['email'], ]
               send_mail( subject, message, email_from, recipient_list )
               uid.password = password
               uid.save()
               return render(request,'sign-in.html',{'msg':'New password sent on your Email.'})

          except:
              return render(request,'sign-up.html',{'msg':'Account Does not Exists.'})
    return render(request,'forgot-password.html')

def change_password(request):
    uid = User.objects.get(email = request.session['email'])
    
    if request.method == 'POST':
          uid = User.objects.get(email = request.session['email'])
          if request.POST['password'] == uid.password:
               if request.POST['npassword'] == request.POST['cpassword']:
                    uid.password = request.POST['npassword']
                    uid.save()
                    return render(request,'change-password.html',{'msg':'Password Changed','uid':uid})
               return render(request,'change-password.html',{'msg':'New Passwords are not same.','uid':uid})
          return render(request,'change-password.html',{'msg':'Current Password is Wrong.','uid':uid})
    return render(request,'change-password.html',{'uid':uid})

def cart1(request,pk):
    product = p.objects.get(id=pk)
    uid = User.objects.get(email= request.session['email'])
    Cart.objects.create(
        user = uid,
        product = product,
    )
    # return render(request,'cart.html',{'uid':uid,'product':product})
    return redirect('index')

def delete_cart(request,pk):
    uid = User.objects.get(email=request.session['email'])
    cart = Cart.objects.get(id=pk)
    cart.delete()
    return render(request,'cart.html',{'uid':uid})

# def update_cart(request,pk):
#     uid = User.objects.get(Email=request.session['email'])
#     cart= Cart.objects.get(id=pk)
#     if request.method == 'POST':
#         cart.quantity = request.POST['qty'],

def cart(request):
    uid = User.objects.get(email=request.session['email'])
    cart = Cart.objects.filter(user=uid)
    am=0
    for i in cart:
        am += i.product.product_price
    return render(request,'cart.html',{'uid':uid,'cart':cart,'am':am})    

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def cart(request):

        uid = User.objects.get(email=request.session['email'])
        cart = Cart.objects.filter(user=uid)
        am=0
        buy = Buy.objects.create(
            user = uid
        )
        for i in cart:
            am += i.product.product_price
            Order.objects.create(
                item = i.product,
                buy = buy
            )
        buy.amount = am
        buy.save()
        currency = 'INR'
        amount = am*100




        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'paymenthandler/{buy.id}'
 
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['cart'] = cart
        context['am'] = am
        return render(request, 'cart.html', context=context)

def cart1(request,pk):
        product = p.objects.get(id=pk)
        uid = User.objects.get(email= request.session['email'])
        Cart.objects.create(
         user = uid,
         product = product,
        )
    # return render(request,'cart.html',{'uid':uid,'product':product})
        return redirect('index')

@csrf_exempt
def paymenthandler(request,pk):
    uid = User.objects.get(email=request.session['email'])
    
    # only accept POST request.
    if request.method == "POST":
        try:
                buy = Buy.objects.get(id=pk)
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
 
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(
                params_dict)
                #if result is None:
                amount = buy.amount*100  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    buy.pay_id = payment_id
                    # buy.verify = True
                    buy.save()
                    # render success page on successful caputre of payment
                    return render(request, 'success.html',{'buy':buy,'uid':uid})
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'fail.html',{'uid':uid})
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
# 	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def cart(request):
#     uid = User.objects.get(email=request.session['email'])
#     cart = Cart.objects.filter(user=uid)
#     product = p.objects.get()
    
#     am = 0
#     buy = Buy.objects.create(
#         user = uid 
#     )
#     for i in cart :
#         am += i.product.product_price

#         Cart.objects.create(
#             user = uid,
#             product = product , 
#         )
#     # return render(request,'cart.html',{'cart':cart,'am':am})
#     buy.amount = am 
#     buy.save()
#     currency = 'INR'
#     amount = am*100 

# 	# Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
# 													currency=currency,
# 													payment_capture='0'))

# 	# order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'

# 	# we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
#     context['cart'] = cart
#     context['am'] = am
#     return render(request, 'cart.html', context=context)


# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# def homepage(request):
# 	currency = 'INR'
# 	amount = 20000 # Rs. 200

# 	# Create a Razorpay Order
# 	razorpay_order = razorpay_client.order.create(dict(amount=amount,
# 													currency=currency,
# 													payment_capture='0'))

# 	# order id of newly created order.
# 	razorpay_order_id = razorpay_order['id']
# 	callback_url = 'paymenthandler/'

# 	# we need to pass these details to frontend.
# 	context = {}
# 	context['razorpay_order_id'] = razorpay_order_id
# 	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
# 	context['razorpay_amount'] = amount
# 	context['currency'] = currency
# 	context['callback_url'] = callback_url

# 	return render(request, 'index.html', context=context)

# # @csrf_exempt
# # def paymenthandler(request,pk):

# # # only accept POST request.
# #     if request.method == "POST":

# #         try:

# #             uid = User.objects.get(email=request.session['email'])
            
# #             buy = Buy.objects.grt(id=pk)
# # 		   # get the required parameters from post request.
# # 		    payment_id = request.POST.get('razorpay_payment_id', '')
# # 		    razorpay_order_id = request.POST.get('razorpay_order_id', '')
# # 		    signature = request.POST.get('razorpay_signature', '')
# # 		    params_dict = {
# # 			    'razorpay_order_id': razorpay_order_id,
# # 			    'razorpay_payment_id': payment_id,
# # 			    'razorpay_signature': signature
# # 		    }

# # 			# verify the payment signature.
# # 		    result = razorpay_client.utility.verify_payment_signature(params_dict)
# # 			#if result is None:
# # 			    amount = buy.amount*100 # Rs. 200
# # 			    try:
# # 				    	# capture the payemt
# # 					    razorpay_client.payment.capture(payment_id, amount)
# #                         buy.pay_id = payment_id
# #                         buy.verify = True
# #                         buy.save()
# #                         cart = Cart.objects.filter(user=uid)
# #                         cart.delete()
# # 					    # render success page on successful caputre of payment
# # 					    return render(request, 'success.html',{'buy':buy})
# # 			    except:

# # 					    # if there is an error while capturing payment.
# # 				    	return render(request, 'fail.html')
# # 			#else:

# # 				# if signature verification fails.
# # 			#	return render(request, 'fail.html')
# # 		except:
# # 	    		# if we don't find the required parameters in POST data
# # 	        return HttpResponseBadRequest()
	
# #     else:
# # 	# if other than POST request is made.
# # 	    return HttpResponseBadRequest()

# @csrf_exempt
# def paymenthandler(request,pk):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
            
#             uid = User.objects.get(email=request.session['email'])
#             buy = Buy.objects.get(id=pk)
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             # if result is None:
#             amount =buy.amount*100    # Rs. 200
#             try:
 
#                     # capture the payemt
#                 razorpay_client.payment.capture(payment_id, amount)
#                 buy.pay_id = payment_id
#                 buy.verify = True
#                 buy.save()
#                 cart = Cart.objects.filter(user=uid)
#                 cart.delete()
#                     # render success page on successful caputre of payment
#                 return render(request, 'paymentsuccess.html')
#             except:
 
#                     # if there is an error while capturing payment.
    #             return render(request, 'paymentfail.html')
    #         # else:
 
    #         #     # if signature verification fails.
    #         #     return render(request, 'paymentfail.html')
    #     except:
 
    #         # if we don't find the required parameters in POST data
    #         return HttpResponseBadRequest()
    # else:
    #    # if other than POST request is made.
    #     return HttpResponseBadRequest()