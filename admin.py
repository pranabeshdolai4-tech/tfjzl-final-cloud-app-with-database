from django.contrib import admin
# Seven imported classes from models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# ChoiceInline implementation
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


# QuestionInline implementation
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


# QuestionAdmin implementation
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']


# LessonAdmin implementation
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    inlines = [QuestionInline]


# CourseAdmin with LessonInline & QuestionInline
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register models in admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)