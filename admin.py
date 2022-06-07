from django.contrib import admin
from .models import *

admin.site.register(customer)
admin.site.register(book)
admin.site.register(order)
admin.site.register(tag)