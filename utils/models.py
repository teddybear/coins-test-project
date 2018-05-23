from django.db import models


class MoneyField(models.DecimalField):
    """Special field representing money"""
    def __init__(self, max_digits=6, decimal_places=2, **kwargs):
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, **kwargs)
