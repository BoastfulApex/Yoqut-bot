from django.db import models


class About(models.Model):
    class Meta:
        verbose_name = "About"
        verbose_name_plural = "1.About"

    id = models.AutoField(primary_key=True)
    description_en = models.TextField(verbose_name="About company Ru")
    description_ru = models.TextField(verbose_name="About company En")
    logo = models.CharField(max_length=1000, verbose_name="Company Logo")

    def __str__(self):
        return "about-company"


class FaqModel(models.Model):
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "2.FAQ LINK"

    id = models.AutoField(primary_key=True)
    faq = models.URLField(verbose_name="Faq link")

    def __str__(self):
        return self.faq


class PriceListModel(models.Model):
    class Meta:
        verbose_name = "Price List"
        verbose_name_plural = "3.Price List"

    id = models.AutoField(primary_key=True)
    pirce_list = models.CharField(max_length=1000, verbose_name="Pirce list")

    def __str__(self):
        return f"image - {self.id}"


class PhotoModel(models.Model):
    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "4.Photo"

    id = models.AutoField(primary_key=True)
    photo = models.CharField(max_length=1000, verbose_name="Photo")
    description_ru = models.TextField(verbose_name="Description RU", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description EN", blank=True, null=True)

    def __str__(self):
        return f"image - {self.id}"


class VideoModel(models.Model):
    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "5. Videos"

    id = models.AutoField(primary_key=True)
    video = models.CharField(max_length=1000, verbose_name="Video")
    description_ru = models.TextField(verbose_name="Description RU", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description EN", blank=True, null=True)

    def __str__(self):
        return f"video - {self.id}"


class SerificateModel(models.Model):
    class Meta:
        verbose_name = "Sertificate"
        verbose_name_plural = "6. Sertificates"

    id = models.AutoField(primary_key=True)
    photo = models.CharField(max_length=1000, verbose_name="Photo")
    description_ru = models.TextField(verbose_name="Description RU", blank=True, null=True)
    description_en = models.TextField(verbose_name="Description EN", blank=True, null=True)

    def __str__(self):
        return f"sertificate - {self.id}"