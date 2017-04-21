from zope.annotation import IAnnotations

ANNOTATIONS_KEY = 'collective.customlogin.success'


def update_challenge_status(request, status):
    IAnnotations(request)[ANNOTATIONS_KEY] = status


def get_challenge_status(request):
    return IAnnotations(request).get(ANNOTATIONS_KEY)


def find_context(request):
    """Find the context from the request
    http://stackoverflow.com/questions/10489544/getting-published-content-item-out-of-requestpublished-in-plone
    """
    published = request.get('PUBLISHED', None)
    context = getattr(published, '__parent__', None)
    if context is None:
        context = request.PARENTS[0]
    return context
