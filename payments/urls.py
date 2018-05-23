from django.urls import path
from payments.views import Payments

urlpatterns = [
    path("", Payments.as_view(), name="payments")
]
