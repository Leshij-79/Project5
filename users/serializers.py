from rest_framework.serializers import ModelSerializer

from users.models import CustomUser, UserPayment


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class UserPaymentSerializer(ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"
