from django.db import models
from django.db.models.signals import pre_save


class User(models.Model):
    USER_TYPE_CHOICES = (
        ("user", "USER"),
        ("admin", "ADMIN"),
    )

    class Meta:
        verbose_name = "Foydalanuvchilar"
        verbose_name_plural = "1.Foydalanuvchilar"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(verbose_name="ID", unique=True, default=1)
    lang = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=300, verbose_name="Ismi")
    phone = models.CharField(max_length=300, verbose_name="Telefon", blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name="Aktivligi")
    is_admin = models.CharField(verbose_name="Foydalanuvchi turi", max_length=300,
                                choices=USER_TYPE_CHOICES, default="user", blank=True, null=True)

    def __str__(self):
        return f"{self.user_id}"


class Category(models.Model):
    category_name = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    unique_name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    kirish_narxi = models.PositiveIntegerField(default=0)
    chiqish_narxi = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.unique_name


class AddStorage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.unique_name


class RemoveFrom(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
