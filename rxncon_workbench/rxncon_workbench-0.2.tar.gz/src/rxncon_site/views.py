from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from src.fileTree.models import File
from src.quick_format.models import Quick
import rxncon.input.quick.quick as rxncon_quick
import rxncon.input.excel_book.excel_book as rxncon_excel

# function based view, easier than class based but less strong



def rxncon_site_index(request):
    return render(request, "static_pages/index.html")

def publications(request):
    return render(request, "static_pages/publications.html")

def funding(request):
    return render(request, "static_pages/funding.html")

def support(request):
    return render(request, "static_pages/support.html")

def compare_systems(request, id, system, called_from="File"):
    if called_from == "File":
        instance = File.objects.get(id=id)
        try:
            book = rxncon_excel.ExcelBook(instance.get_absolute_path())
        except:
            raise ImportError("Could not import file")
    else:
        instance = Quick.objects.get(id=id)
        try:
            book = rxncon_quick.Quick(instance.quick_input)
        except:
            raise ImportError("Could not import Quick")

    rxncon_system = book.rxncon_system

    rxns = 0
    for rxn in rxncon_system.reactions:
        if not rxn in system.reactions:
            rxns +=1

    cnts = 0
    for cnt in rxncon_system.contingencies:
        if not cnt in system.contingencies:
            cnts += 1

    return {"rxns": rxns,
            "cnts": cnts}

def guided_tour(request):
    return render(request, "guided_tour.html")
