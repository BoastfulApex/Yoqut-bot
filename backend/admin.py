from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(AddStorage)
admin.site.register(RemoveFrom)

