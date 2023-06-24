from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

class WholeSellers(models.Model):
    ip = models.CharField(max_length=18, primary_key=True)

class Products(models.Model):
    product_id = models.CharField(max_length=15)
    product_name = models.CharField(max_length=30)
    cat = models.CharField(max_length=15)
    subcat = models.CharField(max_length=15)
    ret_price = models.IntegerField()
    ws_price = models.IntegerField()