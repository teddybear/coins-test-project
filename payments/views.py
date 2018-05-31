from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer


class Payments(ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
