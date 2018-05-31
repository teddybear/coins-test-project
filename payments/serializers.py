from django.db import transaction
from rest_framework import serializers
from payments.models import Payment
from accounts.models import Account


class PaymentSerializer(serializers.Serializer):
    from_account = serializers.CharField(max_length=255)
    to_account = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=20, decimal_places=10)

    def validate(self, data):
        """
        Validate payment before saving
        """
        from_account = data["from_account"]
        to_account = data["to_account"]
        amount = data["amount"]

        if amount <= 0:
            raise serializers.ValidationError("Amount must be positive value")

        if from_account == to_account:
            raise serializers.ValidationError("Transfer on the same account")

        try:
            from_account = Account.objects.get(pk=from_account)
        except Account.DoesNotExist:
            raise serializers.ValidationError("from_account does not exist")

        try:
            to_account = Account.objects.get(pk=to_account)
        except Account.DoesNotExist:
            raise serializers.ValidationError("to_account does not exist")

        if from_account.currency != to_account.currency:
            raise serializers.ValidationError("Accounts currencies not equal")

        # data["from_account"] = from_account
        # data["to_account"] = to_account

        return data

    @transaction.atomic
    def create(self, validated_data):
        from_account = validated_data["from_account"]
        to_account = validated_data["to_account"]
        amount = validated_data["amount"]

        from_account = Account.objects.select_for_update().get(pk=from_account)
        to_account = Account.objects.select_for_update().get(pk=to_account)

        from_account.balance = from_account.balance - amount
        to_account.balance = to_account.balance + amount

        payment = Payment.objects.create(
            account=from_account,
            to_account=to_account,
            amount=amount
        )

        from_account.save()
        to_account.save()

        return payment

    def update(self, instance, validated_data):
        raise serializers.MethodNotAllowed("Update Payment is prohibited")
