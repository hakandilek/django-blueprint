from django.db import models

class Visitor(models.Model):
    class Meta:
        db_table = 'track_Visitor'

    session_key = models.CharField(max_length=36)
    client_address = models.CharField(max_length=15)
    client_host = models.CharField(max_length=60, null=True)
    client_user = models.CharField(max_length=60, null=True)
    http_referer = models.CharField(max_length=120, null=True)
    http_host = models.CharField(max_length=120, null=True)
    http_path = models.CharField(max_length=250)
    http_method = models.CharField(max_length=7)
    visit_time = models.DateTimeField(auto_now=True, blank=False)
    
    
