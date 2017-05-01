from django.contrib import admin
from django.conf.urls import include, url

from core.views import HomeView

admin.autodiscover()


urlpatterns =[
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
]
