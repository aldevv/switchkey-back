from django.contrib import admin
from core.models import User, Product, BuyHistory

admin.site.register(User)
admin.site.register(Product)
admin.site.register(BuyHistory)
