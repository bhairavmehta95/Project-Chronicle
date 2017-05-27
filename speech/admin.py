from django.contrib import admin

# Register your models here.

from .models import Student, Enrollments, Class, Topic, Question, Completion, Teacher, Keyword, TopicProgress

admin.site.register(Student)
admin.site.register(Enrollments)
admin.site.register(Class)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Completion)
admin.site.register(Teacher)
admin.site.register(Keyword)
admin.site.register(TopicProgress)