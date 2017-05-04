from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, HttpResponse



def inline_edit_callback(request):
    """
    Callback for the ajax script, to update inline-editable fields.
    """
    content_type_name = request.POST['object_class']
    id = request.POST['object_id']
    field = request.POST['field']
    ct = ContentType.objects.get(model=content_type_name)


    # Get instance
    instance = ct.model_class().objects.get(id=id)

    # Check permissions
    if hasattr(instance, 'has_edit_perm_on_field') and \
                instance.has_edit_perm_on_field(request.user, field):
        value = request.POST['value']
        setattr(instance, field, value)
        instance.save()
    else:
        return HttpResponseForbidden()

    return HttpResponse('OK, Success')

"""
Example:

class Profile(Model):
    def has_edit_perm_on_field(self, user, field):
        return user.is_superuser or self.user_id == user.id
"""
