from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'',                                   include('blueprint.urls')),
    (r'^accounts/',                         include('registration.backends.default.urls')),
)
