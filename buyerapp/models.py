
from distutils.file_util import move_file
from operator import mod
from django.db import models
from seller import models as sm

# Create your models here.
class User(models.Model):

    fname = models.CharField(max_length=40) 
    lname = models.CharField(max_length=40)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=40)
    mobile = models.CharField(max_length=12) 

    def __str__(self):
        return self.fname + ' ' + self.lname  

    #def __str__(self):
        #return self.email 


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = sm.models.ForeignKey(sm.Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
 
    
    def __str__(self):
        return str(self.user) 
# class Cart(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product = models.ForeignKey(sm.Product,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=)

# class Cart(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     product = models.ForeignKey(sm.Product,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)

#     def __str__(self):
#         return self.uid.fname

class Buy(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pay_id =models.CharField(max_length=50,null=True,blank=True)
    amount = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Order(models.Model):
    item = models.ForeignKey(sm.Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    buy = models.ForeignKey(Buy,on_delete=models.CASCADE)