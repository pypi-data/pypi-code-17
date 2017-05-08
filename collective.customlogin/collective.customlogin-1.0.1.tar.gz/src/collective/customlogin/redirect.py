from collective.customlogin.utils import update_challenge_status
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope import schema
from zope.annotation import IAnnotations
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements, Interface


class IRedirectAction(Interface):
    """Interface for the configurable aspects of a redirect action.

    This is also used to create add and edit forms, below.
    """

    url = schema.TextLine(
        title=_(u"Message"),
        description=_(u"The URL to redirect the user to"),
        required=True
    )


class RedirectAction(SimpleItem):
    """The actual persistent implementation of the redirect action element.
    """
    implements(IRedirectAction, IRuleElementData)

    url = ''

    element = 'collective.customlogin.Redirect'

    @property
    def summary(self):
        return _(u"Redirect to ${url}", mapping=dict(url=self.url))


class RedirectActionExecutor(object):
    """The executor for this action.

    This is registered as an adapter in configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, IRedirectAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        request = self.context.REQUEST
        update_challenge_status(request, status=True)
        request.RESPONSE.redirect(self.element.url, lock=1)
        return True


class RedirectAddForm(AddForm):
    """An add form for redirect rule actions.
    """
    form_fields = form.FormFields(IRedirectAction)
    label = _(u"Add Redirect Action")
    description = _(u"A redirect action will redirect the user.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = RedirectAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class RedirectEditForm(EditForm):
    """An edit form for redirect rule actions.

    Formlib does all the magic here.
    """
    form_fields = form.FormFields(IRedirectAction)
    label = _(u"Edit Redirect Action")
    description = _(u"A redirect action will redirect the user.")
    form_name = _(u"Configure element")
