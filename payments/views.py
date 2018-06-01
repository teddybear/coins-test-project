from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from payments.models import Payment
from payments.serializers import PaymentSerializer


class Payments(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_fields = "__all__"
