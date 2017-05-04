
__doc__ = """

Author:             Jonathan Slenders
Short description:  Utility for prefetching data in a single SQL query.

+----------------------------------------------------------------------------------
|Normally, we use Django's `.select_related` to pull related classes in
|a query, but this only works for foreign keys from the query set where we apply
|the .select_related on and not the other way around.
|
|The prefetcher loads the instances of a related model which point through foreign
|keys to any item in the original query set.
+----------------------------------------------------------------------------------


++ ===============================================================================
++ ====== Typical use: the pagination ====================================
++ ===============================================================================
++
++ # Our original query set
++ subscriptions = Subscription.objects.filter(...)
++
++ # We paginate it
++ paginated_subscriptions = paginate(request, subscriptions)
++
++ # Prefetch User profiles (for any visible item on this page)
++ get_profile = make_prefetcher(paginated_subscriptions.object_list, 'user__id', Profile, 'user__id')
++         # NOTE: Profile.user__id points to a Subscription.user__id
++
++ # Render template
++ return { 'subscriptions': paginated_subscriptions, 'get_profile': get_profile }
++
++ # In template
++
++ {% for s in subscriptions %}
++     {% call profile = get_profile s %}
++         {{ profile }}
++ {% endfor %}
++ {# Every call to `Subscription.user.get_profile` would result in a query, but
++    this doesn't #}
++ ===============================================================================
"""

from django.db import models

# See also |mvne/helpdesk/views/search.py| for instance.

def make_prefetcher(object_list, attribute, related, related_attribute):
    """
    For a list of objects `object_list`, load all the instances of
    the class `related_cls` where `related_attribute` points to an `attribute`
    of an object in this list.
    """

    # We can accept managers or objects for the related class
    # This is required in some use cases where the default manager hides
    # a subset of the objects.
    if isinstance(related, models.Manager):
        related_manager = related
    else:
        related_manager = related.objects

    # -
    def get_attribute(object, attribute):
        attrs = attribute.split('__')
        for a in attrs:
            if object and a:
                object = getattr(object, a)
        return object

    # Get IDs for the objects in this list
    object_ids = [ get_attribute(o, attribute) for o in object_list ]

    # Fetch al related objects where the attribute matches
    fetched_objects = list(related_manager.filter(** { '%s__in' % related_attribute: object_ids })
                                    .select_related(related_attribute))

    def prefetcher(obj):
        for o in fetched_objects:
            if get_attribute(o, related_attribute) == get_attribute(obj, attribute):
                return o

    return prefetcher

