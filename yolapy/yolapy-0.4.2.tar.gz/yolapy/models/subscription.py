from yolapy.services import Yola


class Subscription(object):

    """Construct a Subscription.

    :param id: Str, 32 char ID
    :param created_at: Str, creation time
    :param updated_at: Str, last update time
    :param partner_id: Str, ID of the partner
    :param user_id: Str, 32 character ID of the owner
    :param status: Str
    :param term: Str
    :param sku: Str, SKU of the related product
    :param type: Str,
    :param start_date: Str
    :param expiry_date: Str
    :param billing_date: Str
    :param deprovision_date: Str
    :param auto_renew: Bool
    :param properties: Dict

    :return: Subscription
    :rtype: yolapy.models.Subscription

    """

    _fields = (
        'id', 'created_at', 'updated_at', 'partner_id', 'user_id', 'status',
        'term', 'sku', 'type', 'start_date', 'expiry_date', 'billing_date',
        'deprovision_date', 'auto_renew', 'properties')

    def __init__(self, **fields):
        self.client = Yola()
        for field_name in self._fields:
            setattr(self, field_name, fields.get(field_name))

    @classmethod
    def list(cls, **kwargs):
        """Return a filtered list of Subscriptions.

        Usage::

           >>> from yolapy.models import Subscription
           >>> user_id = 'abcdef1234567890abcdef1234567890'
           >>> user_subs = Subscription.list(user_id=user_id)
           >>> print user_subs[0]
           <yolapy.models.subscription.Subscription object>
           >>> print user_subs[0].user_id
           u'abcdef1234567890abcdef1234567890'
        """
        response = Yola().list_subscriptions(**kwargs)
        return [cls(**sub) for sub in response['results']]
