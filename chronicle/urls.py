from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import speech.views
import speech.student
import speech.teacher
import speech.question_interface
import speech.question_builder
import speech.metrics


urlpatterns = [
    # Views - General
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', speech.views.landing, name='landing'),
    url(r'^about/', speech.views.about, name='about'),
    url(r'^demo/$', speech.views.demo, name='demo'),
    url(r'^enroll/', speech.views.enroll, name='enroll'),
    url(r'^login/', speech.views.login_user, name='login'),
    #url(r'^db', speech.views.db, name='db'),

    # Student
    url(r'^signup/', speech.student.signup_user, name='signup'),
    url(r'^logout/$', speech.student.logout_user, name='logout_user'),
    
    # Teacher
    url(r'^teacher/$', speech.teacher.teacher_portal),
    url(r'^teacher/signup/', speech.teacher.signup_teacher),
    url(r'^teacher/createClass/', speech.teacher.createClass),
    url(r'^teacher/getClasses/', speech.teacher.getClasses),
    url(r'^teacher/gettopics/(?P<classKey>[0-9A-Z]{6})/', speech.teacher.getTopics),
    url(r'^teacher/addtopic/', speech.teacher.addTopic),
    url(r'^teacher/ajax/deleteTopic/', speech.teacher.ajaxDeleteTopic),
    url(r'^teacher/ajax/editTopic/', speech.teacher.ajaxEditTopic),
    url(r'^teacher/createQuestion/', speech.teacher.createQuestion),
    url(r'^teacher/ajax/deleteQuestion/', speech.teacher.ajaxDeleteQuestion),
    url(r'^teacher/ajax/getClass', speech.teacher.ajaxGetClass),
    url(r'^teacher/ajax/editClass', speech.teacher.ajaxEditClass),
    url(r'^teacher/ajax/deleteClass', speech.teacher.ajaxDeleteClass),
    url(r'^teacher/ajax/getQuestionsInTopic', speech.teacher.getQuestionsInTopic),
    url(r'^teacher/ajax/addKeyword', speech.teacher.addKeyword),

    # Question Interface
    url(r'^classes/$', speech.question_interface.class_page, name='class_page'),
    url(r'^speech/$', speech.question_interface.speech, name='speech'),
    url(r'^(\d+)/$', speech.question_interface.topic_page, name='topic_page'),
    url(r'^(\d+)/(\d+)/$', speech.question_interface.question_page, name='question_page'),
    url(r'^(\d+)/(\d+)/(\d+)/$', speech.question_interface.speech, name='speech'),

    # Data
    url(r'^getStudentBestScore/(\d+)/', speech.data.getStudentBestScore, name='getStudentBestScore'),

    # Question Builder
    url(r'^builder/(\d+)/(\d+)/$', speech.question_builder.question_builder, name='question_builder'),
    url(r'^builder/(\d+)/(\d+)/(\d+)/$', speech.question_builder.question_builder_existing, name='question_builder_existing'),
    url(r'^buildNewQuestion/', speech.question_builder.build_question),
    url(r'^builder/(\d+)/(\d+)/manualNewQuestion/', speech.question_builder.manual_new_question),

    # Metrics
    url(r'^metrics/$', speech.metrics.metrics, name='metrics'),
    url(r'^metrics/ajax/getStudentPerformance/$', speech.metrics.get_student_performance, name='getStudentPerformance'),
    url(r'^metrics/ajax/getQuestionStatistics/$', speech.metrics.get_question_statistics, name='getQuestionStatistics'),

    # Secret (these are bandaid solutions and I am not proud of them)
    url(r'^secret/$', speech.metrics.secret, name='secret'),
]
