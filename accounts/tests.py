from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from django.contrib.auth.models import User


class TestAccounts(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = cls.client_class()

    def setUp(self):
        alice = User.objects.create_user("alice")
        alice_account = Account.objects.create(
            owner=alice, id="alice123", currency="PHP", balance=1000)

        bob = User.objects.create_user("bob")
        bob_account = Account.objects.create(
            owner=bob, id="bob456", currency="PHP", balance=1000)

        self.url = reverse("api:accounts:account-list")

    def test_list(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.data
        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 2)
        first = data["results"][0]
        self.assertIn("owner", first)
        self.assertIn("balance", first)
        self.assertIn("currency", first)
        self.assertIn("id", first)
        self.assertEqual(first["currency"], "PHP")
