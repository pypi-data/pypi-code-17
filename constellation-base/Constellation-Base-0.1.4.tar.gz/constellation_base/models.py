from django.db import models
from django.contrib.auth.models import Group


class SiteSetting(models.Model):
    organization = models.CharField(max_length=75)
    description = models.CharField(max_length=512, null=True)
    background = models.ImageField(upload_to='background', null=True,
                                   blank=True)


# These will not be available on Mobile
class TitlebarLink(models.Model):
    url = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    settings = models.ForeignKey(SiteSetting, on_delete=models.CASCADE)


class GlobalTemplateSettings():
    def __init__(self, allowBackground):
        self.allowBackground = allowBackground
        self.background = None
        try:
            site_settings = SiteSetting.objects.get(pk=1)
            self.organization = site_settings.organization
            self.description = site_settings.description
            self.background = site_settings.background if self.allowBackground else None
        except SiteSetting.DoesNotExist:
            self.organization = "My Organization"
            self.description = "An organization description will need to be set up in \
            the admin panel"

        try:
            self.titlebar_links = TitlebarLink.objects.all()
        except TitlebarLink.DoesNotExist:
            self.titlebar_links = None

    def settings_dict(self):
        return {
            'background': self.background,
            'description': self.description,
            'organization': self.organization,
            'titlebar_links': self.titlebar_links,
        }


class LocalGroupACLEntry(models.Model):
    """ACL for Local Groups that don't exist in other authentication sources"""
    group = models.ForeignKey(Group)

    # This is a string since the user might not exist at the time they log in
    # and need this to be applied
    username = models.CharField(max_length=150)

    def __str__(self):
        return "{0}: {1}".format(self.group, self.username)

    class Meta:
        verbose_name = "Supplemental Group ACL Entry"
        verbose_name_plural = "Supplemental Group ACL Entries"
