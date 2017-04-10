from .forms import FileForm, DeleteFileForm
import django.forms as forms

from rxncon_site.views import *
from .models import File
from quick_format.models import Quick
from rxncon.input.excel_book.excel_book import ExcelBook

def file_detail(request, id, compare_dict = None):
    instance = File.objects.get(id=id)
    slug = File.objects.filter(id=id).values("slug")
    project_files = File.objects.filter(slug=slug).order_by("-updated")
    try:
        book = ExcelBook(instance.get_absolute_path())
    except Exception as e:
        raise ImportError("Could not import file")
    rxncon_system = book.rxncon_system

    context_data = {
        "project_files": project_files,
        "title": instance.project_name,
        "instance": instance,
        "nr_reactions": len(rxncon_system.reactions),
        "nr_contingencies": len(rxncon_system.contingencies),
        "loaded": instance.loaded,
    }

    if compare_dict:
        context_data.update(compare_dict)

    return render(request, "file_detail.html", context_data)


def file_compare(request, id):
    loaded = File.objects.filter(loaded=True)
    if loaded:
        try:
            loaded_rxncon = ExcelBook(loaded[0].get_absolute_path())
        except:
            raise ImportError("Could not import file")

    else:
        loaded = Quick.objects.get(loaded=True)
        try:
            loaded_rxncon = rxncon_quick.Quick(loaded.quick_input)
        except:
            raise ImportError("Could not import quick")


    loaded_rxncon_system = loaded_rxncon.rxncon_system

    differences = compare_systems(request, id, loaded_rxncon_system)

    compare_dict = {
        "compare_nr_reactions": len(loaded_rxncon_system.reactions),
        "compare_nr_contingencies": len(loaded_rxncon_system.contingencies),
        "nr_different_reactions": differences["rxns"],
        "nr_different_contingencies": differences["cnts"],
    }


    return file_detail(request, id, compare_dict)


def file_upload(request, slug= None):
    # TODO: like this, it is not case sensitive. "Elefant" and "elefant" are the same project
    form = FileForm(request.POST or None, request.FILES or None)
    context = {}
    if slug != None: # add file to existing project
        try:
            file = File.objects.filter(slug=slug)[0]
            project_name = file.project_name
            form = FileForm(request.POST or None, request.FILES or None, initial={'project_name': project_name})
            form.fields['project_name'].widget = forms.HiddenInput()

            context.update({
                'add_to_project': True,
                'project_name': project_name,
            })

        except KeyError:
            pass

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context.update({
        "form": form,
    })
    return render(request, "file_form.html", context)

def file_delete(request, pk):
    f = get_object_or_404(File, pk=pk)
    project_name = f.project_name
    timestamp = f.timestamp
    filename = f.get_filename()
    slug = f.slug
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, instance=f)

        if form.is_valid(): # checks CSRF
            f.delete_file_from_harddisk()
            f.delete()
            other_file_id = str(File.objects.filter(project_name=project_name).latest("updated").id)
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/files/"+other_file_id+"/") # wherever to go after deleting
    else:
        form = DeleteFileForm(instance=f)

    template_vars = {'form': form,
                     'project_name': project_name,
                     "timestamp": timestamp,
                     "file": filename,
                     }
    return render(request, 'file_delete.html', template_vars)

def file_delete_project(request, slug):
    project = File.objects.filter(slug=slug).order_by("-updated")
    f = project[0] # latest file
    project_name = f.project_name
    timestamp = f.timestamp
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, instance=f)
        if form.is_valid(): # checks CSRF
            f.delete_project_from_harddisk()
            project.delete()
            messages.success(request, "Successfully deleted")
            return HttpResponseRedirect("/") # wherever to go after deleting
    else:
        form = DeleteFileForm(instance=f)
    template_vars = {'form': form,
                     'project': project_name,
                     "timestamp": timestamp,
                        }
    return render(request, 'file_delete.html', template_vars)

def file_load(request, id):
    File.objects.all().update(loaded=False)
    Quick.objects.all().update(loaded=False)
    target = File.objects.filter(id=id)
    target.update(loaded=True)
    if target[0].loaded:
        messages.info(request, "File '" + target[0].get_filename() + "' successfully loaded")
    return file_detail(request, id)


