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
