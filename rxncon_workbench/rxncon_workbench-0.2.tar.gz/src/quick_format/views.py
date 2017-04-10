from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import os
import rxncon.input.quick.quick as rxncon_quick
import rxncon.input.excel_book.excel_book as rxncon_excel
from src.rxncon_site.views import *




from .models import Quick
from src.fileTree.models import File
from .forms import QuickForm, DeleteQuickForm


def quick_detail(request, id, compare_dict=None):
    instance = Quick.objects.get(id=id)
    rxncon_system = rxncon_quick.Quick(instance.quick_input)

    context_data = {
        "title": instance.name,
        "instance": instance,
        "nr_reactions": len(rxncon_system.rxncon_system.reactions),
        "nr_contingencies": len(rxncon_system.rxncon_system.contingencies),
        "loaded": instance.loaded,
    }

    if compare_dict:
        context_data.update(compare_dict)

    return render(request, "quick_detail.html", context_data)


def quick_compare(request, id):
    loaded = File.objects.filter(loaded=True)
    if loaded:
        try:
            loaded_rxncon = rxncon_excel.ExcelBook(loaded[0].get_absolute_path())
        except:
            raise ImportError("Could not import file")

    else:
        loaded = Quick.objects.get(loaded=True)
        try:
            loaded_rxncon = rxncon_quick.Quick(loaded.quick_input)
        except:
            raise ImportError("Could not import quick")

    loaded_rxncon_system = loaded_rxncon.rxncon_system

    differences = compare_systems(request, id, loaded_rxncon_system, called_from="Quick")

    compare_dict = {
        "compare_nr_reactions": len(loaded_rxncon_system.reactions),
        "compare_nr_contingencies": len(loaded_rxncon_system.contingencies),
        "nr_different_reactions": differences["rxns"],
        "nr_different_contingencies": differences["cnts"],
    }


    return quick_detail(request, id, compare_dict)


def quick_new(request):
    # TODO: like this, it is not case sensitive. "Elefant" and "elefant" are the same project
    form = QuickForm(request.POST or None, request.FILES or None)
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        filename = instance.slug + "_quick_definition.txt"
        model_path = "%s/%s/%s/%s" % (media_root, instance.slug, "description", filename)
        os.mkdir("%s/%s" % (media_root, instance.slug))
        os.mkdir("%s/%s/%s" % (media_root, instance.slug, "description"))

        with open(model_path, mode='w') as f:
            f.write(instance.quick_input)

        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context={
        "form": form,
    }
    return render(request, "quick_form.html", context)


def quick_delete(request, id):
    q = get_object_or_404(Quick, id=id)
    if request.method == 'POST':
        form = DeleteQuickForm(request.POST, instance=q)

        if form.is_valid(): # checks CSRF
            q.delete_from_harddisk()
            q.delete()
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/") # wherever to go after deleting
    else:
        form = DeleteQuickForm(instance=q)
    template_vars = {'form': form,
                     'name': q.name,
                     'timestamp': q.timestamp,
                     'quick_input': q.quick_input,
                     "download": q.get_download_url()
                     }
    return render(request, 'quick_delete.html', template_vars)

def quick_update(request, id=None):
    instance = get_object_or_404(Quick, id=id)
    form = QuickForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context_data = {
        "title": instance.name,
        "instance":instance,
        "form": form,
    }
    return render(request, "quick_form.html", context_data)

def quick_load(request, id):
    File.objects.all().update(loaded=False)
    Quick.objects.all().update(loaded=False)
    target = Quick.objects.filter(id=id)
    target.update(loaded=True)
    if target[0].loaded:
        messages.info(request, "Quick definition '" + target[0].name + "' successfully loaded")
    return quick_detail(request, id)

# def quick_save(request, id):
#     q = get_object_or_404(Quick, id=id)
#     q.download_system_description()


