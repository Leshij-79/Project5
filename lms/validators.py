from rest_framework import serializers


class UrlLessonValidator:
    def __call__(self, value):
        if "youtube.com" in value.lower():
            return True
        else:
            raise serializers.ValidationError("Ссылки на ресурсы кроме YouTube.com запрещены")
