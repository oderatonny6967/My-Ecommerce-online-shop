from django.contrib import admin

#first import the models to appear in the admin page  
from .models import Product,Order,Customer,Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)