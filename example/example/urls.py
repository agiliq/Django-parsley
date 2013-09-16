from django.contrib import admin
from django.conf.urls import patterns, url, include

from core.views import HomeView

admin.autodiscover()


urlpatterns = patterns('core.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
)
