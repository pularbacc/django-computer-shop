from django.contrib import admin
from order.models import *

# Register your models here.


admin.site.register(Payment)
admin.site.register(Orders)
admin.site.register(Orders_detail)
admin.site.register(Cart)