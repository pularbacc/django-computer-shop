from django.contrib import admin
from product.models import *

# Register your models here.


admin.site.register(Product_Type)
admin.site.register(Manufacturer)
admin.site.register(Product)
# mainboard
admin.site.register(Socket_CPU)
admin.site.register(Chipset)
admin.site.register(RAM_type)
admin.site.register(Mainboard_Form)
admin.site.register(Mainboard)
# CPU 
admin.site.register(CPU_Series)
admin.site.register(CPU_Generation)
admin.site.register(CPU)
# Card đồ họa
admin.site.register(GPU)
admin.site.register(Memory_Standard)
admin.site.register(VGA)
# RAM
admin.site.register(RAM)
# Ổ cứng
admin.site.register(Connection_standard)
admin.site.register(Hard_Drive)
# Nguồn máy tính 
admin.site.register(PSU_Performance)
admin.site.register(PSU)
# Vỏ máy 
admin.site.register(CaseType)
admin.site.register(Colors)
admin.site.register(CASE_Cover)
admin.site.register(Mainboard_Support)
# Quạt tản nhiệt
admin.site.register(Heatsink)
admin.site.register(Radiator)
admin.site.register(Socket_Support)