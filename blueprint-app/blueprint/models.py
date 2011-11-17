from django.db import models
from django.utils.encoding import force_unicode
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

STATUS = (
          ('N', 'new'),
          ('C', 'confirmed'),
          ('D', 'declined'),
          )

class Sample(models.Model):
    name = models.CharField(max_length=250)
    status = models.CharField(max_length=3, choices=STATUS, default='N', blank=False)
    class Meta:
        db_table = 'Sample'
    