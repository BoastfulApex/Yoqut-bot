from typing import List, Any
from asgiref.sync import sync_to_async
from backend.models import *


@sync_to_async
def add_user(user_id, name, phone, email, lang):
    try:
        return User(user_id=int(user_id), name=name, phone=phone, email=email, lang=lang).save()
    except Exception as err:
        print(err)


@sync_to_async
def get_user(user_id: int):
    try:
        user = User.objects.filter(user_id=user_id).first()
        return user
    except:
        return None


@sync_to_async
def get_users() -> List[User]:
    try:
        users = User.objects.filter(is_admin="user").all()
        return users
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def set_lang(lang, user_id):
    user = User.objects.filter(user_id=user_id).first()
    user.lang = lang
    user.save()


@sync_to_async
def get_lang(user_id):
    try:
        user = User.objects.filter(user_id=user_id).first()
        if user.lang:
            return user.lang
        else:
            return "en"
    except:
        "en"


@sync_to_async
def get_categories() -> List[Category]:
    try:
        categories = Category.objects.all()
        return categories
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def add_product(unique_name, kirish_narxi, chiqish_narxi, category):
    try:
        return Product(unique_name=unique_name, kirish_narxi=kirish_narxi, chiqish_narxi=chiqish_narxi,
                       category=category).save()
    except Exception as err:
        print(err)


@sync_to_async
def get_products() -> List[Product]:
    try:
        products = Product.objects.all()
        return products
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_category(id: int):
    try:
        category = Category.objects.filter(id=id).first()
        return category
    except:
        return None


@sync_to_async
def get_product(id: int):
    try:
        category = Product.objects.filter(id=id).first()
        return category
    except:
        return None


@sync_to_async
def add_Storage(product, count):
    try:
        return AddStorage(product=product, count=count).save()
    except Exception as err:
        print(err)


@sync_to_async
def get_storage() -> List[AddStorage]:
    try:
        storage = AddStorage.objects.all()
        return storage
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_storage_product(id: int):
    try:
        storage = AddStorage.objects.filter(id=id).first()
        return storage
    except:
        return None


@sync_to_async
def sell_Storage(product, count):
    try:
        return RemoveFrom(product=product, count=count).save()
    except Exception as err:
        print(err)


@sync_to_async
def sell_Storages_get() -> List[RemoveFrom]:
    try:
        storage = RemoveFrom.objects.all()
        return storage
    except Exception as err:
        print("ERROR ->>>>", err)
        return None


@sync_to_async
def get_by_serial(serial: str):
    try:
        storage = RemoveFrom.objects.filter(product__unique_name=serial)
        return storage
    except:
        return None

# @sync_to_async
# def get_categories() -> List[Product]:
#     items = Product.objects.distinct("category_name")
#     return items
#
#
# @sync_to_async
# def get_category_by_name(category_name) -> List[ProductCategory]:
#     category = ProductCategory.objects.get(category_name=category_name)
#     return category
#
#
# @sync_to_async
# def get_items(category) -> List[Product]:
#     return Product.objects.all().filter(category_code=category).all()
#
#
# @sync_to_async
# def get_item(item_id) -> Product:
#     item = Product.objects.filter(id=int(item_id)).first()
#     return item
#
#
# @sync_to_async
# def get_purchase(user) -> List[CartModel]:
#     try:
#         purchase = CartModel.objects.filter(user=user, is_success=False).order_by("-id")
#         return purchase
#     except:
#         pass
#
#
# @sync_to_async
# def get_purchase_by_id(purchase_id):
#     try:
#         purchase = CartModel.objects.get(id=purchase_id)
#         return purchase
#     except:
#         pass
#
#
# @sync_to_async
# def delete_purchase(purchase_id):
#     purchase = CartModel.objects.get(id=purchase_id)
#     purchase.delete()
#
#
# @sync_to_async
# def update_purchase(buyer):
#     purchase = False
#     purchases = CartModel.objects.filter(user=buyer).all()
#     for purchase in purchases:
#         purchase.is_success = True
#         purchase.save()
#
#     return purchase
#
#
# @sync_to_async
# def get_about_us():
#     try:
#         about_us = About.objects.all().order_by("-id")[0]
#         return about_us
#     except Exception as err:
#         print(err)
#         return None
#         pass
#
#
# @sync_to_async
# def get_faq():
#     try:
#         faq = FaqModel.objects.all().order_by("-id")[0]
#         return faq
#     except Exception as err:
#         print(err)
#         return None
#         pass
#
#
# @sync_to_async
# def get_price_list():
#     try:
#         price_list = PriceListModel.objects.all().order_by("-id")[0]
#         return price_list
#     except Exception as err:
#         print(err)
#         return None
#         pass
#
#
# @sync_to_async
# def get_videos():
#     try:
#         videos = VideoModel.objects.all().order_by("-id")
#         return videos
#     except:
#         return None
#
#
# @sync_to_async
# def get_photos():
#     try:
#         photos = PhotoModel.objects.all().order_by("-id")
#         return photos
#     except:
#         return None
#
#
# @sync_to_async
# def get_certificate():
#     try:
#         certificates = SerificateModel.objects.all().order_by("-id")
#         return certificates
#     except:
#         return None
