import logging
from django import forms
from django_dragonpay.utils import decrypt_data
from django_dragonpay import settings as dp_settings

logger = logging.getLogger('dragonpay.forms')


class DragonpayCallbackForm(forms.Form):
    '''Dragonpay form for Name-Value Pair model where data is sent via
    HTTP GET callbacks.'''

    STATUS_CODES = [
        ('S', 'Success'), ('F', 'Failure'), ('P', 'Pending'),
        ('U', 'Unknown'), ('R', 'Refund'), ('K', 'Chargeback'),
        ('V', 'Void'), ('A', 'Authorized')]

    txnid = forms.CharField(max_length=128)
    refno = forms.CharField(max_length=32)
    status = forms.CharField(max_length=1)
    message = forms.CharField(max_length=128)
    digest = forms.CharField(max_length=40)
    param1 = forms.CharField(max_length=128, required=False)
    param2 = forms.CharField(max_length=128, required=False)

    def clean(self):
        '''Custom clean method to verify the message authenticity thru
        the digest.'''

        from django_dragonpay.utils import get_dragonpay_digest

        KEYS = ['txnid', 'refno', 'status', 'message']
        to_digest = ':'.join([self.cleaned_data[key] for key in KEYS])

        digest = get_dragonpay_digest(to_digest)

        # Validate that the message sent is cryptographically valid
        if self.cleaned_data['digest'] != digest:
            logger.error(
                'Request hash [%s] doesnt match caclulated [%s]',
                self.cleaned_data['digest'], digest)

            forms.ValidationError("DragonPay digest doesn't match!")

        # Decrypt params if they are encrypted
        if dp_settings.DRAGONPAY_ENCRYPT_PARAMS:
            for key in ['param1', 'param2']:
                param = self.cleaned_data.get(key)

                if param:
                    self.cleaned_data[key] = decrypt_data(param)
                    logger.debug(
                        'Decrypting %s:%s', param, self.cleaned_data[key])

        return self.cleaned_data
