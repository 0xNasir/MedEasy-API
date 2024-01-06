from django.contrib.auth.models import User
from django.db import models

# Create your models here.
"""
Defining model here.
"""


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    expired_on = models.DateField()
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product_info = models.FileField(upload_to='info/')

    def __str__(self):
        return self.name

    """
    Get the total price of product based on quantity and unit price.
    Total price will be calculated multiplying quantity and unit_price.
    """

    def calculateTotalPrice(self):
        return self.quantity * self.unit_price

    """
    Get available in stock product. 
    If quantity of a product is greater than 0, we consider it as available in stock.
    """

    def availableInStock(self):
        return self.quantity > 0
