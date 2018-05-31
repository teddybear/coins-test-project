from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import Account
from payments.models import Payment
from django.contrib.auth.models import User


class TestPayments(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = cls.client_class()

    def setUp(self):
        alice = User.objects.create_user("alice")
        self.alice_account = Account.objects.create(
            owner=alice, id="alice123", currency="PHP", balance=1000)

        bob = User.objects.create_user("bob")
        self.bob_account = Account.objects.create(
            owner=bob, id="bob456", currency="PHP", balance=1000)

        self.url = reverse("api:payments:payments")

    def test_payment(self):
        """Test case successful payment"""
        data = {
            "from_account": self.alice_account.id,
            "to_account": self.bob_account.id,
            "amount": 100
        }
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.data
        self.assertIn("status", data)
        self.assertIn("payment_id", data)
        self.assertEqual(data["status"], "OK")
        pay_id = data["payment_id"]
        self.assertTrue(Payment.objects.filter(pk=pay_id).exists())
        bob = Account.objects.get(pk=self.bob_account.id)
        alice = Account.objects.get(pk=self.alice_account.id)
        self.assertEqual(alice.balance, 900)
        self.assertEqual(bob.balance, 1100)

    def test_payment_account_not_exist(self):
        """Test case nonexistant account payment"""
        data = {
            "from_account": "nonex",
            "to_account": self.bob_account.id,
            "amount": 100
        }
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = resp.data
        self.assertIn("non_field_errors", resp_data)
        self.assertEqual(len(resp_data["non_field_errors"]), 1)
        self.assertEqual(
            resp_data["non_field_errors"][0], "from_account does not exist")

        data["from_account"] = self.alice_account.id
        data["to_account"] = "nonex"

        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = resp.data
        self.assertIn("non_field_errors", resp_data)
        self.assertEqual(len(resp_data["non_field_errors"]), 1)
        self.assertEqual(
            resp_data["non_field_errors"][0], "to_account does not exist")

    def test_payment_same_account(self):
        """Test case same account payment"""
        data = {
            "from_account": self.bob_account.id,
            "to_account": self.bob_account.id,
            "amount": 100
        }
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = resp.data
        self.assertIn("non_field_errors", resp_data)
        self.assertEqual(len(resp_data["non_field_errors"]), 1)
        self.assertEqual(
            resp_data["non_field_errors"][0], "Transfer on the same account")

    def test_payment_neg_amount(self):
        """Test case payment with negative amount"""
        data = {
            "from_account": self.bob_account.id,
            "to_account": self.bob_account.id,
            "amount": -100
        }
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = resp.data
        self.assertIn("non_field_errors", resp_data)
        self.assertEqual(len(resp_data["non_field_errors"]), 1)
        self.assertEqual(
            resp_data["non_field_errors"][0], "Amount must be positive value")

    def test_payment_different_currency(self):
        """Test case payment with different currencies on accounts"""
        self.bob_account.currency = "USD"
        self.bob_account.save()
        data = {
            "from_account": self.alice_account.id,
            "to_account": self.bob_account.id,
            "amount": 100
        }
        resp = self.client.post(self.url, data=data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp_data = resp.data
        self.assertIn("non_field_errors", resp_data)
        self.assertEqual(len(resp_data["non_field_errors"]), 1)
        self.assertEqual(
            resp_data["non_field_errors"][0], "Accounts currencies not equal")
