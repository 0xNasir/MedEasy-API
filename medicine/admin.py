from django.contrib import admin

from medicine.models import Product

# Register your models here.

"""
This file will play role in admin backend.
list_display: It will display the table of column in admin backend for product model.
list_filter: It will show filter option at right side.
search_fields: A search filter will be shown at top of product table. User can search product by name.
list_per_page: Display 20 items per page.
"""


class productAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    list_display = ['name', 'quantity', 'unit_price', 'expired_on', 'added_on', 'added_by']
    list_filter = ['expired_on']
    search_fields = ['name']
    list_per_page = 20


admin.site.register(Product, productAdmin)
