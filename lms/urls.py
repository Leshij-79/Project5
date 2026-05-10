from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonDetailAPIView,
                       LessonListAPIView, LessonRetrieveUpdateAPIView, LessonUpdateAPIView,
                       SubscriptionsAPIView)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),
    path("lessons/<int:pk>/retrieve/", LessonRetrieveUpdateAPIView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/destory/", LessonDestroyAPIView.as_view(), name="lesson_destroy"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("subscription/", SubscriptionsAPIView.as_view(), name="subscription"),
]

urlpatterns += router.urls
