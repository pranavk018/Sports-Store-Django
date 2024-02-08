from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Cricket'),(2,'Football'),(3,'Swimming'))
    #no need to add id, it will be by default
    name=models.CharField(max_length=50,verbose_name='Product Name')
    price=models.FloatField()
    details=models.CharField(max_length=100, verbose_name='Product details')
    cat=models.IntegerField(verbose_name='Category',choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name='Available')
    pimage = models.ImageField(upload_to='image',default=1)


class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE,db_column='uid')
    pid = models.ForeignKey(Product,on_delete = models.CASCADE,db_column='pid')
    quantity = models.IntegerField(default = 1)

class Order(models.Model):
    order_id=models.IntegerField()
    sid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='sid')
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)

