from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonDetailAPIView,
    LessonListAPIView,
    LessonRetrieveUpdateAPIView,
    LessonUpdateAPIView,
    SubscriptionsAPIView, CoursePaymentCreateAPIView,
)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/retrieve/", LessonRetrieveUpdateAPIView.as_view(), name="lesson-retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/destory/", LessonDestroyAPIView.as_view(), name="lesson-destroy"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("subscription/<int:pk>/", SubscriptionsAPIView.as_view(), name="subscription"),
    # path("subscription/", SubscriptionsAPIView.as_view(), name="subscription"),  # На долгую память
    path("payment_course/<int:pk>/", CoursePaymentCreateAPIView.as_view(), name="payment-create"),
]

urlpatterns += router.urls
