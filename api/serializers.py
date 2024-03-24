from rest_framework import serializers
from api.models import Entry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"


class CreateEntrySerializer(serializers.ModelSerializer):
    subject = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        model = Entry
        fields = ["subject", "message"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
