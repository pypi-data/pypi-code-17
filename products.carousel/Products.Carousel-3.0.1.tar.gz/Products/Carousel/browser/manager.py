from Acquisition import aq_base
from zope.interface import alsoProvides
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.Carousel.interfaces import ICarouselFolder
from Products.Carousel.utils import addPermissionsForRole
from Products.Carousel.config import CAROUSEL_ID

class CarouselManager(BrowserView):

    def __call__(self):

        if hasattr(self.context.aq_base, CAROUSEL_ID):
            carousel = getattr(self.context, CAROUSEL_ID)
        else:
            pt = getToolByName(self.context, 'portal_types')
            newid = pt.constructContent(
                            type_name='Folder',
                            container=self.context,
                            id='carousel',
                            title='Carousel Banners'
                        )
            carousel = getattr(self.context, newid)

            # exclude the (Archetypes or Dexterity) folder from navigation
            if hasattr(aq_base(carousel), 'setExcludeFromNav'):
                carousel.setExcludeFromNav(True)
            elif hasattr(aq_base(carousel), 'exclude_from_nav'):
                carousel.exclude_from_nav = True

            # mark the new folder as a Carousel folder
            alsoProvides(carousel, ICarouselFolder)

            # make sure Carousel banners are addable within the new folder
            addPermissionsForRole(carousel, 'Manager',
                                  ('Carousel: Add Carousel Banner',))
            addPermissionsForRole(carousel, 'Site Administrator',
                                  ('Carousel: Add Carousel Banner',))

            # make sure *only* Carousel banners are addable
            aspect = ISelectableConstrainTypes(carousel)
            aspect.setConstrainTypesMode(1)
            aspect.setLocallyAllowedTypes(['Carousel Banner'])
            aspect.setImmediatelyAddableTypes(['Carousel Banner'])

            carousel.reindexObject()

        self.request.RESPONSE.redirect(
            carousel.absolute_url() + '/@@edit-carousel'
        )

