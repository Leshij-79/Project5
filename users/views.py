from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser, UserPayment
from users.serializers import UserSerializer, UserPaymentSerializer


class UsersViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserPaymentListAPIView(ListAPIView):
    queryset = UserPayment.objects.all()
    serializer_class = UserPaymentSerializer