from __future__ import unicode_literals

from django.db import models


# Create your models here.

class categoryItem(models.Model):
    """
        Definie categorys for information.
        It will also define menuentry items and sections created
    """
    
    itemCategory    = models.CharField(max_length=50, unique=True)    # Reference
    itemActive      = models.IntegerField(default=0)    # Defines display of the item in menu
    loggedOnly      = models.IntegerField(default=1)    # Defines if it is visible only to logged users
    itemOrder       = models.IntegerField(default=0)     # Defines de appearing order in menu. If 0 (zero) don't show on menus
    showOnTopMenu   = models.IntegerField(default=0)     # If = 1, defines if category shows on HomePage top menu

    itemDescription = models.CharField(max_length=50, null=True, blank=True) # Alternative text to itemCategory
    onMouseOverDescription = models.CharField(max_length=50, null=True, blank=True) # Alternative Text to display onMouseOver
    #itemLayout      = models.ForeignKey('itemLayout', 'itemLayoutName', null=True, blank=True) # Which kind of display? Links to block template
    #itemTemplate    = models.CharField("Alternative itemTemplate (by default, the category name):",max_length=50, null=True, blank=True) # Alternate display form
    itemTemplate    = models.ForeignKey('itemLayout', 'itemLayoutName', null=True, blank=True) # Alternate display form
    itemsByLine    = models.IntegerField(default=0, null=True, blank=True) # How Many items by line

    itemReadMore    = models.CharField("Label to 'Read More' buttom", default="Ver +", max_length=50, null=True, blank=True) # Mouse Over info
    itemLinkTo      = models.CharField("linkTo - Default: itemCategory", max_length=150, null=True, blank=True) # Mouse Over info

    def __unicode__(self):
        #return str(self.itemOrder)+"  - " + str(self.itemCategory)+"  - " + str(self.itemActive) 
        return self.itemCategory 

class itemLayout(models.Model):
    """
        List of Block Layouts that each section should have
        Each one correspond to a block template resindin in templates/omCms/sectionLayouts/[itemLayoutName].html
    """
    itemLayoutName = models.CharField(max_length=50, null=False, blank=False, unique=True)
    itemLayoutSortDescription = models.CharField(max_length=150, null=True, blank=True)
    itemLayoutDescription = models.TextField(null=True, blank=True)
    
    def __unicode__(self):
        """
        itemName =  str(self.itemLayoutName)
        
        if self.itemLayoutSortDescription is not None:
            itemName += " - "+str(self.itemLayoutSortDescription)
        
        return itemName
        """
        return str(self.itemLayoutName) + str("" if self.itemLayoutSortDescription is None else " - "+str(self.itemLayoutSortDescription))

class siteMainInfo(models.Model):
    """
        Basic informations about site
    """
    mediaImgUploadTo = 'siteImages/'

    recordReference = models.CharField(max_length = 50, null=False, blank=False, unique=True)
    siteName        = models.CharField(max_length = 50, null=True, blank=True)
    siteLogo        = models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True)
    siteLogoHeigth  = models.IntegerField(null=True, blank=True, default=0)
    siteLogoWidth  = models.IntegerField(null=True, blank=True, default=0)
    siteLogoPadding  = models.IntegerField(null=True, blank=True, default=0)
    siteMenuLeftPadding  = models.IntegerField(null=True, blank=True, default=0)

    siteLogoText  = models.CharField(max_length=50,  null=True, blank=True, default="")
    siteLogoLinkTo  = models.CharField(max_length=50,  null=True, blank=True, default="")

    siteHeadBgImg   = models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True)
    siteHeadrHeigth  = models.IntegerField(null=True, blank=True, default=0)
    siteHeaderWidth  = models.IntegerField(null=True, blank=True, default=0)

    siteBannerImg   = models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True)
    siteBannerHeigth  = models.IntegerField(null=True, blank=True, default=0)
    siteBannerWidth  = models.IntegerField(null=True, blank=True, default=0)

    siteShortDescription = models.CharField(max_length = 150, null=True, blank=True)
    siteHomeLabel       = models.CharField(max_length = 50, null=True, blank=True) # Label for "Home" NavBar reference
    showSiteHomeLabel   = models.BooleanField(default=True) # Define if "Home" should be shown
    siteTagLine1    = models.CharField(max_length = 150, null=True, blank=True)
    siteTagLine2    = models.CharField(max_length = 150, null=True, blank=True)
    siteLongDescription = models.CharField(max_length = 250, null=True, blank=True)
    
    siteAnalytics = models.CharField(max_length = 250, null=True, blank=True)

    siteAdress = models.CharField(max_length = 250, null=True, blank=True)
    sitePhone1 = models.CharField(max_length = 250, null=True, blank=True)
    sitePhone2 = models.CharField(max_length = 250, null=True, blank=True)
    siteEmail = models.CharField(max_length = 250, null=True, blank=True)

    displayLogo     = models.BooleanField(default=True)
    displayImageHeader = models.BooleanField(default=True)
    displayNavBar    = models.BooleanField(default=True)
    displayDrawerMenu = models.BooleanField(default=True)
    allwaysDisplayDrawerMenu = models.BooleanField(default=True)
    displaySlideShow = models.BooleanField(default=True)

    #active = models.BooleanField(default=False, unique=True) # Define wich record is active. Only one can be active 
    #siteTheme = models.CharField(max_length = 250, null=True, blank=True) # Define the Theme to be used 
    siteTheme = models.ForeignKey('theme', 'themeName', null=True, blank=True) # Define t1he Theme to be used in the site, from the list of definined available themes 
    active = models.IntegerField(default=0, unique=True) # Define wich record is active. Only one can be active 

    def __unicode__(self):
        return str(self.recordReference+" - "+str(self.active))

class siteSocialMediaReference(models.Model):
    """
        Links to Social Media
    """
    mediaImgUploadTo = 'socialMediaImages/'
    smName = models.CharField(max_length=50)
    smLogo = models.ImageField(upload_to=mediaImgUploadTo, null=True)
    smLink = models.CharField(max_length=100)

class contentArticle(models.Model):
    """
        Main Content Articles
    """
    mediaImgUploadTo = 'articleImages/'

    articleCategory =   models.ForeignKey('categoryItem', 'itemCategory', null=True, blank=True)
    title           =   models.CharField(max_length=150) 
    slug            =   models.SlugField(null=True, blank=True)
    subTitle        =   models.CharField(max_length=150, null=True, blank=True) 
    teaser          =   models.TextField(null=True, blank=True) 
    teaserImage     =   models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True) 
    
    title1          =   models.CharField(max_length=150, null=True, blank=True) 
    body1Image      =   models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True) 
    body1           =   models.TextField(null=True, blank=True) 
    
    title2          =   models.CharField(max_length=150, null=True, blank=True) 
    body2Image      =   models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True)
    body2           =   models.TextField(null=True, blank=True) 

    title3          =   models.CharField(max_length=150, null=True, blank=True) 
    body3Image      =   models.ImageField(upload_to=mediaImgUploadTo, null=True, blank=True) 
    body3           =   models.TextField(null=True, blank=True) 

    articleFooter   =   models.CharField(max_length=150, null=True, blank=True) 
    
    order = models.IntegerField(default=0, null=True, blank=True) # Appearence order
    active = models.IntegerField(default=0, null=True, blank=True) # Should the article be displayed?

    def __unicode__(self):
        
        if self.articleCategory is None:
            artCat = ""
        else:
            artCat = self.articleCategory.itemCategory

        #print type(self.articleCategory) 
        # self.articleCategory.itemCategory

        #return self.title + " - " + artCat +" - " + str(self.active)
        return self.title + str("" if self.articleCategory is None else " - "+str(self.articleCategory)) +" - " + str(self.active)
        #return self.title + " - " + str(self.active)

class theme(models.Model):
    """
        List the available Themes to be applied to site.
        Will be available in Theme Choice in siteMainInfo.
        Must have corresponding folder and structure manually created. 

        TODO: Make a 'new theme' structure, that will copy from skeleton
    """

    themeName           = models.CharField(max_length = 50, null=False, blank=False, unique=True)
    themeDescription    = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.themeName

