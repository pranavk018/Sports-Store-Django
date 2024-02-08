from django.contrib import admin
from productapp.models import Product, Cart
# Register your models here.

#admin.site.register(Product)
# the above registration, registers the Product Model for Admin view in admin portal
# However, the display columns depend upon the __str__ defined within the Product model

# if we need to display all the columns, comment line 5 and  then we can use below code
class ProductAdmin(admin.ModelAdmin):
    #in order to display specific column, mention them below
    list_display=['id','name','cat','price','details','is_active','pimage'] 
    # in order to apply the filters, mention the following
    # here, while accessing admin panel, check which all filters are applied
    # or clear the filer every time after applying, before new filter is applied
    list_filter=['cat','price','is_active']
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','uid','pid','quantity']
admin.site.register(Cart,CartAdmin)
