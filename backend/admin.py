from django.contrib import admin
from .models import User, Product, ProductCategory, CartModel, Order
from django.contrib.auth.models import Group
admin.site.unregister(Group)



class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Product", {'fields': ["name", "name_ru","price", "description_ru", "description_en", "photo"]}),
        ("About Product", {'fields': ["photo_2","photo_3","photo_4","photo_5","photo_6", "description_2_ru", "description_2_en"]}),
        ("Category/SubCategory", {"fields": ["category_name"]}),
    ]
    list_display = ("name", "category_name","category_name_ru" ,"price")
    list_display_links = ("name", "category_name")


admin.site.register(Product, ProductAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "email", "phone", "is_admin", "is_active")
    list_display_links = ("user_id", "name")


admin.site.register(User, UserAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "category_name_ru")
    list_display_links = ("category_name", "category_name_ru")


admin.site.register(ProductCategory,ProductCategoryAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "amount","total", "is_success")
    list_display_links = ("product", "user")


admin.site.register(CartModel,CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "email", "phone", "company_name", "total", "is_success")
    list_display_links = ("user", "name")


admin.site.register(Order,OrderAdmin)

