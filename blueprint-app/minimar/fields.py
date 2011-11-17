# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from minimar.widgets import MoneyWidget, MoneyHiddenWidget
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MoneyField(forms.MultiValueField):
    widget = MoneyWidget
    hidden_widget = MoneyHiddenWidget
    default_error_messages = {
        'invalid_value': _(u'Enter a valid value.'),
        'invalid_currency': _(u'Enter a valid currency.'),
    }

    def __init__(self, currencies=(), *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.DecimalField(error_messages={'invalid': errors['invalid_value']} ),
            forms.ChoiceField(error_messages={'invalid': errors['invalid_currency']}, choices=currencies),
        )
        super(MoneyField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        logger.debug('compress:%s' % data_list)
        if data_list:
            # Raise a validation error if value or currency is empty
            # (possible if MoneyField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_value'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_currency'])
            return (data_list[0], data_list[1])
        return None
