from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='상품명')
    desc = models.TextField(blank=True)
    amount = models.PositiveIntegerField(verbose_name='결제금액')
    photo = models.ImageField()

    def __str__(self):
        return self.name

