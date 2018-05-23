from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer


class Payments(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Returns list of payments
        Example GET response:
        ```
        {
            "payments": [
                {
                    "account": "alice123",
                    "amount": 400,
                    "to_account": "bob456",
                    "direction": "outgoing"
                },
                {
                    "account": "bob456",
                    "amount": 400,
                    "from_account": "alice123",
                    "direction": "incoming"
                }
            ]
        }
        ```
        """
        queryset = Payment.objects.all()
        result = []
        for payment in queryset:
            result.append({
                "account": payment.account.id,
                "amount": payment.amount,
                "to_account": payment.to_account.id,
                "direction": "outgoing"
            })
            result.append({
                "account": payment.to_account.id,
                "amount": payment.amount,
                "from_account": payment.account.id,
                "direction": "incoming"
            })
        return Response({"payments": result})

    def post(self, request):
        """
        Creates payment transfer

        Example POST request:
        ```
        {
            "from_account": "bob456",
            "to_account": "alice123",
            "amount": 400
        }
        ```

        Example POST response:
        ```
        {
            "status": "OK",
            "payment_id": 10
        }
        ```
        """
        data = JSONParser().parse(request)
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            payment = serializer.save()
            return Response(
                {"status": "OK", "payment_id": payment.id},
                status=status.HTTP_201_CREATED)
