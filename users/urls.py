from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UsersViewSet, UserPaymentListAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UsersViewSet)

urlpatterns = [
    path("users/payments/", UserPaymentListAPIView.as_view(), name="payments_list"),
]

urlpatterns += router.urls
