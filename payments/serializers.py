from django.db import transaction
from rest_framework import serializers
from payments.models import Payment
from accounts.models import Account


class PaymentSerializer(serializers.ModelSerializer):
    from_account = serializers.CharField(max_length=255, source="account")
    to_account = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=20, decimal_places=10)
    direction = serializers.CharField(max_length=8, read_only=True)

    class Meta:
        model = Payment
        exclude = ("id",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret["direction"] == "incoming":
            ret["from_account"] = ret["to_account"]
            del ret["to_account"]
        return ret

    def validate(self, data):
        """
        Validate payment before saving
        """
        from_account = data["account"]
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

        if from_account.balance < amount:
            raise serializers.ValidationError(
                "Insufficient funds on from_account")

        return data

    @transaction.atomic
    def create(self, validated_data):
        from_account = validated_data["account"]
        to_account = validated_data["to_account"]
        amount = validated_data["amount"]

        from_account = Account.objects.select_for_update().get(pk=from_account)
        to_account = Account.objects.select_for_update().get(pk=to_account)

        from_account.balance = from_account.balance - amount
        to_account.balance = to_account.balance + amount

        outgoing_payment = Payment.objects.create(
            account=from_account,
            to_account=to_account,
            amount=amount,
            direction="outgoing"
        )
        Payment.objects.create(
            account=to_account,
            to_account=from_account,
            amount=amount,
            direction="incoming"
        )

        from_account.save()
        to_account.save()

        return outgoing_payment

    def update(self, instance, validated_data):
        raise serializers.MethodNotAllowed("Update Payment is prohibited")
