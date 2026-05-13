from django.contrib import admin

from lms.models import Course, Lesson, Subscriptions, CoursePayment


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


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "user",
    )
    list_filter = ("course",)
    search_fields = ["user", "course"]


@admin.register(CoursePayment)
class CoursePaymentAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "user",
        "amount",
        "session_id",
        "link",
        "status",
    )
    list_filter = (
        "course",
        "user",
        "status",
    )
    search_fields = ["course", "user", "status"]
