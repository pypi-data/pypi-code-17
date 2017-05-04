from django.contrib import admin
from django.utils.encoding import force_text
from django.utils.translation import gettext, gettext_lazy as _


def send_to_trash(modeladmin, request, queryset):
    """
    Trashes all objects in a query.
    """
    del modeladmin, request

    for item in queryset.all():
        item.trash()


def restore_from_trash(modeladmin, request, queryset):
    """
    Restores all objects in a query.
    """
    del modeladmin, request

    for item in queryset.all():
        item.restore()


class TrashedListFilter(admin.SimpleListFilter):
    """
    A filter that only displays trashed model items.
    """
    title = _('trash status')
    parameter_name = 'trashed_at'

    @staticmethod
    def lookups(request, modeladmin):
        del request, modeladmin
        return (
            ('available', gettext('Not in trash')),
            ('trashed', gettext('In trash')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(trashed_at=None)
        if self.value() == 'trashed':
            return queryset.exclude(trashed_at=None)


class TrashableAdminMixin(admin.ModelAdmin):
    """
    Adds trash/restore functionality to a model admin. This'll only work if the underlying model
    supports it.
    """
    actions = [send_to_trash, restore_from_trash]
    list_filter = (TrashedListFilter,)
