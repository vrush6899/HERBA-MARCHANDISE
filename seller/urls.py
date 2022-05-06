from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index3,name='index3'),
    path('login/',views.login,name='login'),
    path('sign-up1/',views.sign_up1,name='sign-up1'),
    path('otp1/',views.otp1,name='otp1'),
    path('forgot-password1/',views.forgot_password1,name='forgot-password1'),
    path('logout/',views.logout,name='logout'),
    path('product/',views.product,name='product'),
    path('view/',views.view,name='view'),
    path('delete-product/<int:pk>',views.delete_product,name='delete-product'),
    #path('delete-service/<int:pk>',views.delete_service,name='delete-service'),
    path('edit-product/<int:pk>',views.edit_product,name='edit-product'),



]