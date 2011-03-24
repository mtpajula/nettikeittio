from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/*$', 'recipes.views.base'),
    (r'^recipes/$', 'recipes.views.list'),
    (r'^recipes/(?P<recipe_id>\d+)/$', 'recipes.views.detail'),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.CSS_ROOT
    }),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.JS_ROOT
    }),


    # Example:
    # (r'^nettikeittio/', include('nettikeittio.foo.urls')),



    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
