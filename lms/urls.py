from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateApiView, LessonDestroyApiView, LessonDetailApiView,
                       LessonListApiView, LessonRetrieveUpdateApiView, LessonUpdateApiView)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonDetailApiView.as_view(), name="lesson_detail"),
    path("lessons/<int:pk>/retrieve/", LessonRetrieveUpdateApiView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/destory/", LessonDestroyApiView.as_view(), name="lesson_destroy"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"),
]

urlpatterns += router.urls
