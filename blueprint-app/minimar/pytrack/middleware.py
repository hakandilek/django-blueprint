'''
Created on Jun 14, 2011

    py-track middleware
    
@author: hd
'''
from minimar.pytrack.models import Visitor
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class TrackVisitorMiddleware(object):
    def process_request(self, request):
        if request.session:
            expire = datetime(2030, 12, 31)
            request.session.set_expiry(expire)
            logger.debug('session_key: %s' % request.session.session_key)
            session_key_ = request.session.session_key
        client_addr_ = request.META.get('REMOTE_ADDR', None)
        client_host_ = request.META.get('REMOTE_HOST', None)
        client_user_ = request.META.get('REMOTE_USER', None)
        http_refe_ = request.META.get('HTTP_REFERER', None)
        http_host_ = request.META.get('HTTP_HOST', None)
        http_path_ = request.get_full_path()
        http_meth_ = request.method
        
        visitor = Visitor(session_key = session_key_, client_address = client_addr_, client_host=client_host_, client_user = client_user_, 
                          http_referer = http_refe_, http_host = http_host_, http_path = http_path_, http_method = http_meth_)
        logger.debug('visitor: %s' % visitor)
        visitor.save()

    def process_response(self, request, response):
        return response
