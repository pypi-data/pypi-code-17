from django.shortcuts import render

from .models import categoryItem
from .models import siteMainInfo
from .models import siteSocialMediaReference
from .models import contentArticle


# Create your views here.

def baseIndex(request):
    """
        Home page index
    """

    context = {}

    siteInfoData = siteMainInfo.objects.get(active=1)

    categorysList = categoryItem.objects.filter(itemActive=1).filter(itemOrder__gt=0).order_by('itemOrder')

    articlesList = contentArticle.objects.filter(active=1).order_by('order')
    articlesListHomePage = contentArticle.objects.filter(active=1).filter(articleCategory__itemCategory__contains='homepage').order_by('order')
    
    context['siteInfoData'] = siteInfoData
    #context['siteTheme']  = str(context['siteInfoData'].siteTheme.themeName)

    context['categorysList'] = categorysList
    context['articlesList'] = articlesList
    context['articlesListHomePage'] = articlesListHomePage

    siteTheme =  siteInfoData.siteTheme.themeName if siteInfoData.siteTheme.themeName else "omCms"

    template = "omCmsMain/themes/"+siteTheme+"/index.html"

    return render(request, template, context)

def categoryArticleDetail(request, category="", article_id=0):
    """
        Detail for Article  in category
    """
    
    context = {}

    siteInfoData = siteMainInfo.objects.get(active=1)
    categorysList = categoryItem.objects.filter(itemActive=1).filter(itemOrder__gt=0).order_by('itemOrder')

    article = contentArticle.objects.get(pk=article_id)

    context['siteInfoData'] = siteInfoData
    context['categorysList'] = categorysList
    context['category'] = category
    context['article_id'] = article_id
    context['article'] = article

    siteTheme =  siteInfoData.siteTheme.themeName if siteInfoData.siteTheme.themeName else "omCms"

    template = "omCmsMain/themes/"+siteTheme+"/detail.html"

    return render(request, template, context)
