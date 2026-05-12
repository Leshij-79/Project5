from icecream import ic
from rest_framework import serializers, request
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscriptions
from lms.validators import UrlLessonValidator


class LessonSerializer(ModelSerializer):
    url_video = serializers.URLField(validators=[UrlLessonValidator()], required=False)

    class Meta:
        model = Lesson
        # validators = [UrlLessonValidator(field='url_video')]
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)
    course = LessonSerializer(many=True, read_only=True)  # course <=> related_name="course"
    subs_course = serializers.SerializerMethodField(read_only=True)  # subs_course <=> related_name="subs_course"

    def get_count(self, obj):
        return obj.course.count()

    def get_subs_course(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.subs_course.filter(course=obj, user=request.user).count()
        return 0

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionsSerializer(ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = "__all__"
