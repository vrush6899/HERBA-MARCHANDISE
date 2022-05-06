from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name='index'),
   #path('index1/',views.index1,name='index1'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('otp/',views.otp,name='otp'),
    path('log-out/',views.log_out,name='log-out'),
    path('blog/',views.blog,name='blog'),
    path('cart/',views.cart,name='cart'),
    path('category/',views.category,name='category'),
    path('confirmation/',views.confirmation,name='confirmation'),
    path('contact/',views.contact,name='contact'),
    path('edit-profile/',views.edit_profile,name='edit-profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('single-blog/',views.single_blog,name='single-blog'),
    path('single-product/',views.single_product,name='single-product'),
    path('checkout/',views.checkout,name='checkout'),
    path('tracking/',views.tracking,name='tracking'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    #path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    #path('view-cart/',views.view_cart, name='view-cart'),
    path('cart1/<int:pk>',views.cart1,name='cart1'),
    #path('cart1/paymenthandler/<int:pk>',views.paymenthandler,name='paymenthandler'),
    path('cart/paymenthandler/<int:pk>', views.paymenthandler, name='paymenthandler'),
    path('delete-cart/<int:pk>',views.delete_cart,name='delete-cart'),
    

]