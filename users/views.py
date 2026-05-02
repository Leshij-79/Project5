from rest_framework.filters import SearchFilter, OrderingFilter
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
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('payment_date',)
