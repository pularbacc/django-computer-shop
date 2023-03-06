from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Suplier, Customer

# Register your models here.


admin.site.register(Customer, UserAdmin)
admin.site.register(Suplier)