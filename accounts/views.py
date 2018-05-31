from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountList(ListAPIView):
    """
    Returns list of accounts
    Example GET response:
    ```
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "alice123",
                "owner": "alice",
                "balance": "133.0000000000",
                "currency": "PHP"
            },
            {
                "id": "bob456",
                "owner": "bob",
                "balance": "234.0000000000",
                "currency": "PHP"
            }
        ]
    }
    ```
    """
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
