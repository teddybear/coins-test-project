from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from accounts.consts import CURRENCIES


class Account(models.Model):
    """Model representing user's accounts
    We use regular User as an owner"""

    id = models.CharField(max_length=255, primary_key=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts")
    balance = models.DecimalField(
        max_digits=20, decimal_places=10, default=Decimal(0))
    currency = models.CharField(max_length=3, choices=CURRENCIES)

    def __str__(self):
        return f"{self.id}"
