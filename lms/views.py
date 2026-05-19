from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, CoursePayment, Lesson, Subscriptions
from lms.paginators import PagePagination
from lms.serializers import CoursePaymentSerializer, CourseSerializer, LessonSerializer, SubscriptionsSerializer
from lms.services import (create_stripe_payment_status, create_stripe_price, create_stripe_products,
                          create_stripe_session)
from lms.tasks import send_email_update
from users.permissions import IsModerator, IsNotModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = PagePagination

    # def get_serializer_context(self):  # использование в API
    #     context = super().get_serializer_context()
    #     context.update({'request': self.request})
    #     return context

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
        send_email_update.delay(serializer.data)


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

    def perform_update(self, serializer):
        serializer.save()
        send_email_update.delay(serializer.data)


class LessonRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModerator | IsOwner,
    )

    def perform_update(self, serializer):
    serializer.save()
    send_email_update.delay(serializer.data)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner, IsNotModerator)

    def perform_destroy(self, instance):
        data = LessonSerializer(instance).data
        instance.delete()
        send_email_update.delay(data)


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


class CoursePaymentCreateAPIView(CreateAPIView):
    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs["pk"]

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

        payment = CoursePayment.objects.filter(user=user, course=course).first()

        if payment:
            return Response(
                {"message": "Оплата по этому курсу уже существует", "payment_link": payment.link},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_id, product_name = create_stripe_products(course)
        price = create_stripe_price(course.price, product_id)
        session_id, session_url = create_stripe_session(price)

        payment = CoursePayment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            session_id=session_id,
            link=session_url,
            status="open",
        )

        return Response(
            {"message": "Ссылка на оплату успешно создана", "payment_link": session_url, "payment_id": payment.id},
            status=status.HTTP_201_CREATED,
        )

    # def perform_create(self, serializer):
    #     payment = serializer.save(user=self.request.user)


class CoursePaymentStatusAPIView(APIView):
    queryset = CoursePayment.objects.all()
    serializer_class = CoursePaymentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        payment_id = kwargs["pk"]

        try:
            payment = CoursePayment.objects.get(id=payment_id)
        except Course.DoesNotExist:
            return Response({"error": "Оплата не найдена"}, status=status.HTTP_404_NOT_FOUND)

        session_id = payment.session_id
        status_payment = create_stripe_payment_status(session_id)

        payment.status = status_payment
        payment.save()

        return Response(
            {"message": "Cтатус оплаты успешно обновлен", "status": status_payment, "payment_id": payment.session_id},
            status=status.HTTP_200_OK,
        )
