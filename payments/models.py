from django.db import models
from accounts.models import Account
from payments.consts import PAYMENT_DIRECTIONS


class Payment(models.Model):
    """Model representing Payment from one account to another"""

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="payments")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    direction = models.CharField(max_length=8, choices=PAYMENT_DIRECTIONS)

    def save(self, *args, **kwargs):
        if not self._state.adding and self.pk is not None:
            raise ValueError("Updating Payment is prohibited")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account} {self.amount}"\
            f" {self.to_account} {self.direction}"
