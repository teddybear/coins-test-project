from django.db import models
from accounts.models import Account
from utils.models import MoneyField


class Payment(models.Model):
    """Model representing Payment from one account to another"""

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="out_payments")
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="in_payments")
    amount = MoneyField(null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self._state.adding and self.pk is not None:
            raise ValueError("Updating Payment is prohibited")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account} {self.amount} {self.to_account}"
