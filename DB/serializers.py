from rest_framework import serializers
from DB.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

class WholeSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholeSellers
        fields = ('ip')

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            'product_id',
            'product_name',
            'cat',
            'subcat',
            'ret_price',
            'ws_price'
        )
