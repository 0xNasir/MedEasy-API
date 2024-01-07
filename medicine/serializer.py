from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from medicine.models import Product

"""
This will serialize the product data from model instance to python native datatype.
Then it will render to json for API response.

"""


class ProductSerializer(ModelSerializer):
    availableInStock = serializers.BooleanField(read_only=True)
    calculateTotalPrice = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['added_by']


"""
User information will be yeilded in product item as a nested object of key 'added_by',
This will be applied only in retrieve and list API endpoints.
"""


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


"""
This serializer class will be invoked in retrieve and list api endpoints.
added_by key value is overriden here for better data visualization.
"""


class RetrieveProductSerializer(ModelSerializer):
    availableInStock = serializers.BooleanField(read_only=True)
    calculateTotalPrice = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    added_by = UserSerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['added_by']
