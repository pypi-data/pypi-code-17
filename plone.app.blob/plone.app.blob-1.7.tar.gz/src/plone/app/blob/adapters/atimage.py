# -*- coding: utf-8 -*-
from plone.app.blob.adapters.atfile import BlobbableATFile
from Products.ATContentTypes.interface import IATImage
from zope.component import adapts


class BlobbableATImage(BlobbableATFile):
    """ adapter for ATImage objects to work with blobs """
    adapts(IATImage)

    def feed(self, blob):
        """ see interface ... """
        data = self.context.getImageAsFile()
        if data is None:
            return
        blobfile = blob.open('w')
        blobfile.write(data.read())     # TODO: use copy or an iterator!!
        blobfile.close()
