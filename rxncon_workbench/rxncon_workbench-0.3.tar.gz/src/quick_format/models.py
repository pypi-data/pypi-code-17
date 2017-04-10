from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import render_to_response
from django.utils.text import slugify
from graphs.models import Graph_from_File
from boolean_model.models import Bool_from_rxnconsys
from rule_based.models import Rule_based_from_rxnconsys
import os
import shutil



class Quick(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    loaded = models.BooleanField(default=False)
    quick_input = models.TextField(null=False)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)  # initial timestamp will be saved one time
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  # auto_now refers to every modification,
    # updated gets reset when Post is updated -duh
    reg_graph = models.ForeignKey(Graph_from_File, null=True, on_delete=models.SET_NULL, blank=True, related_name="regulatory_graph_quick")
    rea_graph = models.ForeignKey(Graph_from_File, null=True, on_delete=models.SET_NULL, blank=True, related_name="reaction_graph_quick")
    boolean_model = models.ForeignKey(Bool_from_rxnconsys, null=True, on_delete=models.SET_NULL, blank=True, related_name="bool_quick")
    rule_based_model = models.ForeignKey(Rule_based_from_rxnconsys, null=True, on_delete=models.SET_NULL, blank=True, related_name="rule_based_quick")


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quick_format:quick_detail", kwargs={"id": self.id})

    def load(self):
        pass

    def get_download_url(self):
        media_url= settings.MEDIA_URL
        # return media_url+"%s" %(self.file)
        # media_root = settings.MEDIA_ROOT
        filename = self.slug + "_quick_definition.txt"
        return "%s%s/%s/%s" % (media_url, self.slug, "description", filename)

    def delete_from_harddisk(self):
        # TODO: test if works in dockers
        media_root = settings.MEDIA_ROOT
        filename = self.slug + "_quick_definition.txt"
        path = "%s/%s/" % (media_root, self.slug)
        shutil.rmtree(path)

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug=slugify(instance.name)



pre_save.connect(pre_save_post_receiver, sender=Quick)