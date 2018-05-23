from rest_framework import serializers
from accounts import models


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Accounts model, currently owner be represented with
    one's username
    """
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = models.Account
        fields = "__all__"
