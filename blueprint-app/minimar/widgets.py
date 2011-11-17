# -*- coding: utf-8 -*-
from django import forms
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MoneyWidget(forms.MultiWidget):
    """
    A Widget that splits money input into two <input type="text"> boxes.
    """
    
    def __init__(self, attrs=None, currencies=None):
        if currencies:
            self.currencies = currencies
        else:
            self.currencies = ()
        widgets = (forms.TextInput(attrs=attrs),
                   forms.Select(attrs=attrs, choices=self.currencies))
        super(MoneyWidget, self).__init__(widgets, attrs)
        #raise RuntimeError("0")

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def render(self, name, value, attrs=None):
        logger.debug('render: %s' %value)
        return super(MoneyWidget, self).render(name, value, attrs)

class MoneyHiddenWidget(MoneyWidget):
    """
    A Widget that splits money input into two <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, attrs=None, currencies=None):
        super(MoneyHiddenWidget, self).__init__(attrs, currencies)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True
