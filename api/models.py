from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Entry(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Kullanıcı Adı"
    )
    subject = models.CharField(max_length=256, verbose_name="Konu")
    message = models.TextField(verbose_name="Mesaj")
    create_date = models.DateTimeField(
        default=timezone.now, verbose_name="Oluşturulma Tarihi"
    )

    class Meta:
        verbose_name = "Kayıt"
        verbose_name_plural = 4 * " " + "Tanım: Kayıtlar"
