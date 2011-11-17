from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^$',                                   'blueprint.views.index'),
    (r'^sample/$',                            'blueprint.views.sample_index'),
    (r'^sample/new$',                         'blueprint.views.sample_create'),
    (r'^sample/edit/(?P<key>[ \S]+)/$',       'blueprint.views.sample_edit'),
    (r'^sample/delete/(?P<key>[ \S]+)/$',     'blueprint.views.sample_delete'),
    (r'^sample/json/$',                       'blueprint.views.sample_json'),
)
