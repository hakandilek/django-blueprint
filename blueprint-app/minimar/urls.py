from django.conf.urls.defaults import *

# Uncomment the next line to enable the admin:
#admin.autodiscover()

urlpatterns = patterns('',
    (r'^user/json/$',                   'minimar.views.user_json'),
)
