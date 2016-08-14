from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import speech.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', speech.views.login_user, name='login'),
    url(r'^db', speech.views.db, name='db'),
    url(r'^signup/', speech.views.signup_user, name='signup'),
    url(r'^login/', speech.views.login_user, name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^classes/$', speech.views.class_page, name='class_page'),
    url(r'^speech/$', speech.views.speech, name='speech'),
    url(r'^(\d+)/$', speech.views.topic_page, name='topic_page'),
    url(r'^(\d+)/(\d+)/$', speech.views.question_page, name='question_page'),
    url(r'^(\d+)/(\d+)/(\d+)/$', speech.views.speech, name='speech'),
]
