from operator import mod
from unicodedata import name
from django.db import models

# Create your models here.
class Seller(models.Model):

    fname = models.CharField(max_length=40) 
    lname = models.CharField(max_length=40)
    Email = models.EmailField(unique=True) 
    password = models.CharField(max_length=40)
    mobile = models.CharField(max_length=12) 

    def __str__(self):
        return self.fname + ' ' + self.lname  

class Product(models.Model):

    product_owner=models.ForeignKey(Seller,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    #pic= models.FileField(upload_to='profile',default='abc.png')
    product_pic = models.FileField(upload_to='product',default='') 
    product_price= models.IntegerField()
    quantity = models.IntegerField()
    
    
    def __str__(self):
        return self.product_owner.fname + ' > ' + self.product_name  