from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Returns list of accounts
        Example GET response:
        ```
        {
            "accounts": [
                {
                    "id": "alice123",
                    "owner": "alice",
                    "balance": "0.00",
                    "currency": "PHP"
                },
                {
                    "id": "bob456",
                    "owner": "bob",
                    "balance": "400.00",
                    "currency": "USD"
                }
            ]
        }
        ```
        """
        queryset = Account.objects.all()
        serializer = AccountSerializer(queryset, many=True)
        return Response({"accounts": serializer.data})
