from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import CustomUser, UserPayment
from users.serializers import UserPaymentSerializer, UserSerializer


class UsersViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserPaymentListAPIView(ListAPIView):
    queryset = UserPayment.objects.all()
    serializer_class = UserPaymentSerializer
    filter_backends = (
        SearchFilter,
        OrderingFilter,
    )
    search_fields = (
        "payment_course__title",
        "payment_lesson__title",
        "payment_method",
    )
    ordering_fields = ("payment_date",)
