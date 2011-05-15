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
    url(r'^recipes/own/$'                  , own_recipes, name='own_recipes'),
    url(r'^recipes/favourites/$'           , favourite_recipes, name='favourite_recipes'),
    url(r'^users/$'                        , list_users, name='list_users'),
    url(r'^search/$'                       , search, name='search'),
    url(r'^search/recipes/$'               , recipe_search, name='recipe_search_field'),
    url(r'^recipes/(?P<recipe_id>\d+)/$'   , render_detail_recipe, name='recipe_page'),
    url(r'^active/(?P<recipe_id>\d+)/$'    , active, name='active_view'),
    url(r'^editrecipe/(?P<recipe_id>\d+)/$', edit_recipe, name='edit_recipe'),
    url(r'^editrecipe/$'                   , new_recipe, name='new_recipe'),
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
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}, name='image_root'),
        
    url(r'^lookup/ingredient/$'            , ingredient_lookup, name='ingredient_lookup'),
    url(r'^lookup/unit/$'            , unit_lookup, name='unit_lookup'),
    url(r'^ajax/favourite/$'            , favourite_ajax, name='favourite_ajax'),
    url(r'^ajax/comment/$'            , comment_ajax, name='comment_ajax'),

    # Example:
    # (r'^nettikeittio/', include('nettikeittio.foo.urls')),



    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
