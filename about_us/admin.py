from django.contrib import admin
from .models import FaqModel, PriceListModel, SerificateModel, PhotoModel, VideoModel, About

admin.site.register(About)
admin.site.register(FaqModel)
admin.site.register(PriceListModel)
admin.site.register(PhotoModel)
admin.site.register(VideoModel)
admin.site.register(SerificateModel)

