from rest_framework import serializers


class UrlLessonValidator:
    def __call__(self, value):
        if not value:  # Если значение пустое - пропускаем
            return True

        if "youtube.com" in value.lower():
            return True
        else:
            raise serializers.ValidationError("Ссылки на ресурсы кроме YouTube.com запрещены")
