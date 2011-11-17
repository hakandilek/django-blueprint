from django.utils.translation import ugettext as txt
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import delete_object
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import permission_required
from blueprint.models import Sample
from django.utils.datastructures import MultiValueDictKeyError
from minimar.utils import json_encode
from minimar.pytrack.decorators import track_visitor
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

@track_visitor
def index(request, context={}):
    logger.debug('index <-')
    logger.debug('request.user: %s' % request.user)
    context['user'] = request.user
    context['login_backends'] = ('google-oauth2', )
    return render_to_response("blueprint/index.html", context)

@permission_required('blueprint.superuser')
def sample_index(request, context={}, status=None):
    logger.debug('sample_index <-')
    
    q = Sample.objects.all().order_by('name')

    if status:
        q = q.filter(status=status)

    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    logger.debug('pagenum : %d' % pagenum)

    context["title"] = txt('Samples')
    context['result_headers'] = [
                                 {'text'  : txt('name'), },
                                 {'text'  : txt('status'), },
                                 {'text'  : txt('edit'), },
                                 {'text'  : txt('delete'), },
                                 ]
    return object_list(request, q, page=pagenum, paginate_by=10, template_name='blueprint/sample_list.html', extra_context=context)

@permission_required('blueprint.superuser')
def sample_create(request):
    if request.method == 'POST':
        key = request.POST['key']
        name = request.POST['name']
        
        if key:
            sample = Sample(id=key, name=name)
        else:
            sample = Sample(name=name)
        
        logger.debug('name    : %r' % name)
        
        #do save
        new_object = sample.save()
        logger.debug('new_object    : %r' % new_object)
        
        return HttpResponseRedirect(reverse('blueprint.views.sample_index'))
    else: 
        return HttpResponse(txt("invalid request."))

@permission_required('blueprint.superuser')
def sample_edit(request, key=None):
    try:
        p = Sample.objects.get(pk=key)
    except Sample.DoesNotExist:
        raise Http404
    context = {
               'key' : key,
               'name' : p.name,
    }
    return sample_index(request, context);

@permission_required('blueprint.superuser')
def sample_delete(request, key=None):
    return delete_object(request, Sample, object_id=key,
                         post_delete_redirect=reverse('blueprint.views.sample_index'))

def sample_json(request, name=None):
    if name:
        q = Sample.objects.filter(name__istartswith=name).order_by('name')
    else:
        q = Sample.objects.all().order_by('name')
        
    data = json_encode(q, only=['id', 'name'])
    return HttpResponse(data, mimetype="text/plain")
