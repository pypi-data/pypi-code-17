from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from pages.models import Page


@receiver(pre_save, sender=Page)
def pre_save_page(sender, update_fields, instance=None, created=False,
                    **kwargs):
    pre_save.disconnect(pre_save_page, sender=Page)
    new_page = instance
    new_page.slug = slugify(instance.title)
    pre_save.connect(pre_save_page, sender=Page)