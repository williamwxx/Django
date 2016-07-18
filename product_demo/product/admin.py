from django.contrib import admin
from product.models import Category, Keyword, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Keyword)
admin.site.register(Product)