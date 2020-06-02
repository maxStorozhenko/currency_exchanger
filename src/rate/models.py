from django.db import models
from django.utils import timezone

from rate import model_choices as mch
from rate.utils import to_decimal


tz = timezone.get_default_timezone()


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    rate = models.DecimalField(max_digits=7, decimal_places=2)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    currency_type = models.PositiveSmallIntegerField(choices=mch.CURRENCY_TYPE_CHOICES)
    rate_type = models.PositiveSmallIntegerField(choices=mch.RATE_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.rate = to_decimal(self.rate)

    def get_date(self):
        return f'{self.created.astimezone(tz).strftime("%d.%m.%Y %H:%M")}'
