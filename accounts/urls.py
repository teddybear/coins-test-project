from django.urls import path
from accounts.views import AccountList

urlpatterns = [
    path("", AccountList.as_view(), name="account-list")
]
