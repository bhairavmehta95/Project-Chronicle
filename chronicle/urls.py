from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import speech.views
import speech.student
import speech.teacher
import speech.question_interface
import speech.question_builder


urlpatterns = [
    # Views - General
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', speech.views.landing, name='landing'),
    url(r'^about/', speech.views.about, name='about'),
    url(r'^demo/$', speech.views.demo, name='demo'),
    #url(r'^db', speech.views.db, name='db'),

    # Student
    url(r'^signup/', speech.student.signup_user, name='signup'),
    url(r'^login/', speech.student.login_user, name='login'),
    url(r'^logout/$', speech.student.logout_user, name='logout_user'),
    
    # Teacher
    url(r'^teacher/$', speech.teacher.login_teacher),
    url(r'^teacher/signup/', speech.teacher.signup_teacher),

    # Question Interface
    url(r'^classes/$', speech.question_interface.class_page, name='class_page'),
    url(r'^speech/$', speech.question_interface.speech, name='speech'),
    url(r'^(\d+)/$', speech.question_interface.topic_page, name='topic_page'),
    url(r'^(\d+)/(\d+)/$', speech.question_interface.question_page, name='question_page'),
    url(r'^(\d+)/(\d+)/(\d+)/$', speech.question_interface.speech, name='speech'),

    # Question Builder
    url(r'^builder/$', speech.question_builder.question_builder, name='question_builder'),
]
