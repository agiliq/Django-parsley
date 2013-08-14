from django.conf.urls import patterns, url

from core.views import HomeView


urlpatterns = patterns(
    'core.views',
    url(r'^$', HomeView.as_view(), name='home'),
)
