##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Filesystem exporter / importer adapters. """

from csv import reader
from csv import writer
import itertools
import operator
from ConfigParser import ConfigParser
from StringIO import StringIO

from zope.interface import implements
from zExceptions import MethodNotAllowed

from DateTime import DateTime
from Products.GenericSetup.interfaces import IFilesystemExporter
from Products.GenericSetup.interfaces import IFilesystemImporter
from Products.GenericSetup.content import DAVAwareFileAdapter
from Products.GenericSetup.content import _globtest
from Products.CMFCore.utils import getToolByName

#
#   setup_tool handlers
#
def exportSiteStructure(context):
    IFilesystemExporter(context.getSite()).export(context, 'structure', True)

def importSiteStructure(context):
    IFilesystemImporter(context.getSite()).import_(context, 'structure', True)


def encode_if_needed(text, encoding):
    if isinstance(text, unicode):
        result = text.encode(encoding)
    else:
        # no need to encode;
        # let's avoid double encoding in case of encoded string
        result = text
    return result


class FolderishDAVAwareFileAdapter(DAVAwareFileAdapter):
    """ A version of the DAVAwareFileAdapter that uses .properties to store
    the DAV result, rather than its own id. For use in serialising folderish
    objects. """
    
    def _getFileName(self):
        """ Return the name under which our file data is stored.
        """
        return '.properties'

#
#   Filesystem export/import adapters
#
class StructureFolderWalkingAdapter(object):
    """ Tree-walking exporter for "folderish" types.

    Folderish instances are mapped to directories within the 'structure'
    portion of the profile, where the folder's relative path within the site
    corresponds to the path of its directory under 'structure'.

    The subobjects of a folderish instance are enumerated in the '.objects'
    file in the corresponding directory.  This file is a CSV file, with one
    row per subobject, with the following wtructure::

     "<subobject id>","<subobject portal_type>"

    Subobjects themselves are represented as individual files or
    subdirectories within the parent's directory.
    If the import step finds that any objects specified to be created by the
    'structure' directory setup already exist, these objects will be deleted
    and then recreated by the profile.  The existence of a '.preserve' file
    within the 'structure' hierarchy allows specification of objects that
    should not be deleted.  '.preserve' files should contain one preserve
    rule per line, with shell-style globbing supported (i.e. 'b*' will match
    all objects w/ id starting w/ 'b'.

    Similarly, a '.delete' file can be used to specify the deletion of any
    objects that exist in the site but are NOT in the 'structure' hierarchy,
    and thus will not be recreated during the import process.
    """

    implements(IFilesystemExporter, IFilesystemImporter)

    def __init__(self, context):
        self.context = context

    def export(self, export_context, subdir, root=False):
        """ See IFilesystemExporter.
        """
        self._encoding = self.context.getProperty('default_charset', 'utf-8')

        # Enumerate exportable children
        exportable = self.context.contentItems()
        exportable = [x + (IFilesystemExporter(x, None),) for x in exportable]
        exportable = [x for x in exportable if x[1] is not None]

        objects_stream = StringIO()
        objects_csv_writer = writer(objects_stream)
        wf_stream = StringIO()
        wf_csv_writer = writer(wf_stream)
        
        
        if not root:
            subdir = '%s/%s' % (subdir, self.context.getId())

        try:
            wft = self.context.portal_workflow
        except AttributeError:
            # No workflow tool to export definitions from
            for object_id, object, ignored in exportable:
                objects_csv_writer.writerow((object_id, object.getPortalTypeName()))
        else:
            for object_id, object, ignored in exportable:
                objects_csv_writer.writerow((object_id, object.getPortalTypeName()))
            
                workflows = wft.getWorkflowsFor(object)
                for workflow in workflows:
                    workflow_id = workflow.getId()
                    state_variable = workflow.state_var
                    state_record = wft.getStatusOf(workflow_id, object)
                    if state_record is None:
                        continue
                    state = state_record.get(state_variable)
                    wf_csv_writer.writerow((object_id, workflow_id, state))
        
            export_context.writeDataFile('.workflow_states',
                                         text=wf_stream.getvalue(),
                                         content_type='text/comma-separated-values',
                                         subdir=subdir,
                                        )
        
        export_context.writeDataFile('.objects',
                                     text=objects_stream.getvalue(),
                                     content_type='text/comma-separated-values',
                                     subdir=subdir,
                                    )

        
        parser = ConfigParser()

        title = self.context.Title()
        description = self.context.Description()
        # encode if needed; ConfigParser does not support unicode !
        title_str = encode_if_needed(title, self._encoding)
        description_str = encode_if_needed(description, self._encoding)
        parser.set('DEFAULT', 'Title', title_str)
        parser.set('DEFAULT', 'Description', description_str)

        stream = StringIO()
        parser.write(stream)

        try:
            FolderishDAVAwareFileAdapter(self.context).export(export_context, subdir, root)
        except (AttributeError, MethodNotAllowed):
            export_context.writeDataFile('.properties',
                                        text=stream.getvalue(),
                                        content_type='text/plain',
                                        subdir=subdir,
                                        )

        for id, object in self.context.objectItems():

            adapter = IFilesystemExporter(object, None)

            if adapter is not None:
                adapter.export(export_context, subdir)

    def import_(self, import_context, subdir, root=False):
        """ See IFilesystemImporter.
        """
        context = self.context
        if not root:
            subdir = '%s/%s' % (subdir, context.getId())

        objects = import_context.readDataFile('.objects', subdir)
        workflow_states = import_context.readDataFile('.workflow_states', subdir)
        if objects is None:
            return
        
        dialect = 'excel'
        object_stream = StringIO(objects)
        wf_stream = StringIO(workflow_states)

        object_rowiter = reader(object_stream, dialect)
        ours = filter(None, tuple(object_rowiter))
        our_ids = set([item[0] for item in ours])

        prior = set(context.contentIds())

        preserve = import_context.readDataFile('.preserve', subdir)
        if not preserve:
            preserve = set()
        else:
            preservable = prior.intersection(our_ids)
            preserve = set(_globtest(preserve, preservable))

        delete = import_context.readDataFile('.delete', subdir)
        if not delete:
            delete= set()
        else:
            deletable = prior.difference(our_ids)
            delete = set(_globtest(delete, deletable))

        # if it's in our_ids and NOT in preserve, or if it's not in
        # our_ids but IS in delete, we're gonna delete it
        delete = our_ids.difference(preserve).union(delete)

        for id in prior.intersection(delete):
            context._delObject(id)

        existing = context.objectIds()

        for object_id, portal_type in ours:

            if object_id not in existing:
                object = self._makeInstance(object_id, portal_type,
                                            subdir, import_context)
                if object is None:
                    logger = import_context.getLogger('SFWA')
                    logger.warning("Couldn't make instance: %s/%s" %
                                   (subdir, object_id))
                    continue

            wrapped = context._getOb(object_id)

            IFilesystemImporter(wrapped).import_(import_context, subdir)
        
        if workflow_states is not None:
            existing = context.objectIds()
            wft = context.portal_workflow
            wf_rowiter = reader(wf_stream, dialect)
            wf_by_objectid = itertools.groupby(wf_rowiter, operator.itemgetter(0))
        
            for object_id, states in wf_by_objectid:
                if object_id not in existing:
                    logger = import_context.getLogger('SFWA')
                    logger.warning("Couldn't set workflow for object %s/%s as it doesn't exist" %
                                   (context.id, object_id))
                    continue
            
                object = context[object_id]
                for object_id, workflow_id, state_id in states:
                    workflow = wft.getWorkflowById(workflow_id)
                    state_variable = workflow.state_var
                    wf_state = {
                        'action': None,
                        'actor': None,
                        'comments': "Setting state to %s" % state_id,
                        state_variable: state_id,
                        'time': DateTime(),
                        }
                
                    wft.setStatusOf(workflow_id, object, wf_state)
                    workflow.updateRoleMappingsFor(object)
            
                object.reindexObject()
            
        
    
    def _makeInstance(self, id, portal_type, subdir, import_context):

        context = self.context
        subdir = '%s/%s' % (subdir, id)
        properties = import_context.readDataFile('.properties',
                                                 subdir)
        tool = getToolByName(context, 'portal_types')

        try:
            tool.constructContent(portal_type, context, id)
        except ValueError: # invalid type
            return None

        content = context._getOb(id)

        if properties is not None:
            if '[DEFAULT]' not in properties:
                try:
                    FolderishDAVAwareFileAdapter(content).import_(import_context, subdir)
                    return content
                except (AttributeError, MethodNotAllowed):
                    # Fall through to old implemenatation below
                    pass
            
            lines = properties.splitlines()

            stream = StringIO('\n'.join(lines))
            parser = ConfigParser(defaults={'title': '', 'description': 'NONE'})
            parser.readfp(stream)

            title = parser.get('DEFAULT', 'title')
            description = parser.get('DEFAULT', 'description')

            content.setTitle(title)
            content.setDescription(description)

        return content
