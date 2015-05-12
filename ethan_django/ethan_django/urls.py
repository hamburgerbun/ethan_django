from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ethan_django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'ethan.views.home_page', name='home'),
    url(r'game/[A-z0-9]+', 'ethan.views.game_page', name='game'),
)
