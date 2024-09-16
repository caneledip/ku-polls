"""Module for admin."""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Choice will be show for with 3 extra line in Question creation page."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Admin user can create a question and choice from admin page and also set published and end date."""

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date", "end_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "end_date", "is_published", "can_vote"]


admin.site.register(Question, QuestionAdmin)
