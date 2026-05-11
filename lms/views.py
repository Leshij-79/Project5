from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscriptions
from lms.paginators import PagePagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionsSerializer
from users.permissions import IsModerator, IsNotModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = PagePagination

    # def get_serializer_class(self):
    #     pass
    #     if self.action == 'retrieve':
    #         return CourseDetailSerializer
    # return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Moderator").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                IsNotModerator,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
                IsNotModerator,
            )
        elif self.action in ["retrieve", "update", "list"]:
            self.permission_classes = (
                IsAuthenticated,
                IsModerator | IsOwner,
            )
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsNotModerator,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = PagePagination
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner, IsNotModerator)


class SubscriptionsAPIView(APIView):
    serializer_class = SubscriptionsSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs["pk"]

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

        subscription = Subscriptions.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка успешно удалена"
        else:
            Subscriptions.objects.create(user=user, course=course)
            message = "Подписка успешно добавлена"

        return Response({"message": message})


# На долгую память
# class SubscriptionsAPIView(APIView):
#     serializer_class = SubscriptionsSerializer
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         course_id = request.data.get("course_id")
#         course = Course.objects.get(id=course_id)
#
#         subscription = Subscriptions.objects.filter(user=user, course=course)
#
#         ic(subscription.exists())
#
#         if subscription.exists():
#             subscription.delete()
#             message = "Подписка успешно удалена"
#         else:
#             Subscriptions.objects.create(user=user, course=course)
#             message = "Подписка успешно добавлена"
#
#         return Response({"message": message})
