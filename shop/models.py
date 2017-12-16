from django.conf import settings
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='상품명')
    desc = models.TextField(blank=True)
    amount = models.PositiveIntegerField(verbose_name='결제금액')
    photo = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    item = models.ForeignKey(Item)
    name = models.CharField(max_length=100, verbose_name='상품명')
    amount = models.PositiveIntegerField(verbose_name='결제금액')

    class Meta:
        ordering = ('-id',)

