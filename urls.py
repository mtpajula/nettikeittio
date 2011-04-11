from django.conf.urls.defaults import *
import django.contrib.auth.views
import settings
from recipes.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/*$'                            , main_page, name='main_page'),
    url(r'^menu/$'                         , menu, name='menu'),
    url(r'^recipes/$'                      , list_recipes, name='list_recipes'),
    url(r'^search/(?P<page>\d*)$'          , search, name='search'),
    url(r'^recipes/(?P<recipe_id>\d+)/$'   , recipe_detail, name='detail'),
    url(r'^active/(?P<recipe_id>\d+)/$'    , active, name='active_view'),
    url(r'^editrecipe/(?P<recipe_id>\d+)/$', edit_recipe, name='edit_recipe'),
    url(r'^newrecipe/$'                    , new_recipe, name='new_recipe'),
    url(r'^user/(?P<user_id>\d+)/$'        , user_detail, name='user_page'),
    url(r'^newuser/$'                      , new_user, name='new_user'),
    url(r'^edituser/(?P<user_id>\d+)/$'    , edit_user, name='edit_user'),
    url(r'^login/$'                        , 'django.contrib.auth.views.login', 
                                            {'template_name': 'recipes/contentpage/login.html'}, name='nk_login'),
    url(r'^logout/$'                       , 'django.contrib.auth.views.logout', 
                                            {'next_page': '/'}, name='nk_logout'),
    url(r'^register/$'                     , register, name='register'),
    url(r'^help/$'                         , nk_help, name='nk_help'),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.CSS_ROOT}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.JS_ROOT}),
    (r'^img/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/home/mikko/nettikeittio/media', 'show_indexes': True}),

    # Example:
    # (r'^nettikeittio/', include('nettikeittio.foo.urls')),



    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
