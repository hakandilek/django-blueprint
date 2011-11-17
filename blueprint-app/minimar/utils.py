# coding=utf-8
#generic utilities in this file
import logging

import datetime
from decimal import Decimal
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.db.models import Model
from django.db.models import ImageField, FileField
from django.db.models.query import QuerySet
from django.utils.functional import Promise
from django.utils import simplejson as json

def debug(msg):
    logger = logging.getLogger()
    logger.debug(msg)

try:
    # we need it, if we want to serialize query- and model-objects
    # of google appengine within json_encode
    from google import appengine
except:
    appengine = None

try:
    # this is just available since django version 1.0
    # google appengine does not provide this function yet!
    from django.utils.encoding import force_unicode
except Exception:
    import types
    # code copied from django version 1.0
    class DjangoUnicodeDecodeError(UnicodeDecodeError):
        def __init__(self, obj, *args):
            self.obj = obj
            UnicodeDecodeError.__init__(self, *args)

        def __str__(self):
            original = UnicodeDecodeError.__str__(self)
            return '%s. You passed in %r (%s)' % (original, self.obj,
                    type(self.obj))
    
    def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
        """
        Similar to smart_unicode, except that lazy instances are resolved to
        strings, rather than kept as lazy objects.

        If strings_only is True, don't convert (some) non-string-like objects.
        """
        if strings_only and isinstance(s, (types.NoneType, int, long, datetime.datetime, datetime.date, datetime.time, float)):
            return s
        try:
            if not isinstance(s, basestring,):
                if hasattr(s, '__unicode__'):
                    s = unicode(s)
                else:
                    try:
                        s = unicode(str(s), encoding, errors)
                    except UnicodeEncodeError:
                        if not isinstance(s, Exception):
                            raise
                        # If we get to here, the caller has passed in an Exception
                        # subclass populated with non-ASCII data without special
                        # handling to display as a string. We need to handle this
                        # without raising a further exception. We do an
                        # approximation to what the Exception's standard str()
                        # output should be.
                        s = ' '.join([force_unicode(arg, encoding, strings_only,
                                errors) for arg in s])
            elif not isinstance(s, unicode):
                # Note: We use .decode() here, instead of unicode(s, encoding,
                # errors), so that if s is a SafeString, it ends up being a
                # SafeUnicode at the end.
                s = s.decode(encoding, errors)
        except UnicodeDecodeError, e:
            raise DjangoUnicodeDecodeError(s, *e.args)
        return s

def json_encode(data, only=None):
    """
    The main issues with django's default json serializer is that properties that
    had been added to an object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data, only=None):
        ret = None
        # Opps, we used to check if it is of type list, but that fails 
        # i.e. in the case of django.newforms.utils.ErrorList, which extends
        # the type "list". Oh man, that was a dumb mistake!
        if isinstance(data, list):
            ret = _list(data, only)
        # Same as for lists above.
#        elif appengine and isinstance(data, appengine.ext.db.Query):
#            ret = _list(data)
        elif isinstance(data, dict):
            ret = _dict(data, only)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data, only)
        elif isinstance(data, QuerySet):
            # Actually its the same as a list ...
            ret = _list(data, only)
        elif isinstance(data, Model):
            ret = _model(data, only)
#        elif appengine and isinstance(data, appengine.ext.db.Model):
#            ret = _googleModel(data)
        # here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
        elif isinstance(data, basestring):
            ret = unicode(data)
        # see http://code.djangoproject.com/ticket/5868
        elif isinstance(data, Promise):
            ret = force_unicode(data)
        elif isinstance(data, datetime.datetime):
            # For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
            # i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
            ret = str(data).replace(' ', 'T')
        elif isinstance(data, datetime.date):
            ret = str(data)
        elif isinstance(data, datetime.time):
            ret = "T" + str(data)
        else:
            # always fallback to a string!
            ret = data
        return ret
    
    def _model(data, only=None):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            # special FileField handling (they can't be json serialized)
            if isinstance(f, ImageField) or isinstance(f, FileField):
                ret[f.attname] = unicode(getattr(data, f.attname))
            else:
                ret[f.attname] = _any(getattr(data, f.attname), only)
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()

        # ignoring _state and delete properties
        add_ons = [k for k in dir(data) if k not in fields and k not in ('delete', '_state',)]
        for k in add_ons:
            ret[k] = _any(getattr(data, k), only)
            
        if only:
            keys = set(ret.keys())
            for key in keys:
                if key not in only:
                    ret.pop(key, None)
        return ret

    def _googleModel(data, only=None):
        ret = {}
        ret['id'] = data.key().id()
        for f in data.fields():
            ret[f] = _any(getattr(data, f), only)
        return ret

    def _list(data, only=None):
        ret = []
        for v in data:
            ret.append(_any(v, only))
        return ret
    
    def _dict(data, only=None):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v, only)
        return ret
    
    ret = _any(data, only)
    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

