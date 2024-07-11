from django.contrib import admin

#first import the models to appear in the admin page  
from .models import Product,Order,Customer

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)