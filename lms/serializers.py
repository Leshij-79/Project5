from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscriptions
from lms.validators import UrlLessonValidator


class LessonSerializer(ModelSerializer):
    url_video = serializers.URLField(validators=[UrlLessonValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)
    course = LessonSerializer(many=True, read_only=True)  # course <=> related_name="course"

    def get_count(self, obj):
        return obj.course.count()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionsSerializer(ModelSerializer):

    class Meta:
        model = Subscriptions
        fields = "__all__"
