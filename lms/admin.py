from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "preview",
    )
    list_filter = ("title",)
    search_fields = ["name", "description"]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "preview",
        "url_video",
        "course",
    )
    list_filter = ("title",)
    search_fields = ["title", "description"]
