# coding: utf-8
"""
    assetic.layertools  (layertools.py)
    Tools to assist with using arcgis integration with assetic
"""
from __future__ import absolute_import

import arcpy
import pythonaddins
import assetic
import six
from ..config import Config
from .commontools import CommonTools
from .commontools import DummyProgressDialog

class LayerTools(object):
    """
    Class to manage processes that sync Assetic search data to a local DB
    """

    def __init__(self, layerconfig=None):
        
        self.config = Config()
        if layerconfig == None:
            self._layerconfig = self.config.layerconfig
        else:
            self._layerconfig = layerconfig
        self._assetconfig = self._layerconfig.assetconfig
        self.asseticsdk = self.config.asseticsdk

        ##initialise common tools so can use messaging method
        self.commontools = CommonTools()

    def get_layer_config(self,lyr,purpose):
        """
        For the given layer get the config settings. Depending on purpose not
        all config is required, so only get relevant config
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        :param purpose: one of 'create','update','delete','display'
        """
        lyr_config_list = [j for i, j in enumerate(
            self._assetconfig) if j["layer"] == lyr.name]
        if len(lyr_config_list) == 0:
            msg = "No configuration for layer {0}".format(lyr.name)
            self.commontools.new_message(msg)
            return None
        lyr_config = lyr_config_list[0]        

        if purpose in ["create","update"]:
        #build list of arcmap fields to query
            fields = list(six.viewvalues(lyr_config["corefields"]))
            if fields == None:
                msg = "missing 'corefields' configuration for layer {0}".format(
                    lyr.name)
                self.commontools.new_message(msg)
                return
            if "attributefields" in lyr_config:
                attfields = list(six.viewvalues(lyr_config["attributefields"]))
                if attfields != None:
                    fields = fields + attfields
            fields.append('SHAPE@')
        return lyr_config,fields
        
    def create_asset(self,lyr):
        """
        For the given layer create new assets for the selected features only if
        features have no assetic guid.
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        """
        iPass = 0
        iFail = 0

        #get configuration for layer
        lyr_config,fields = self.get_layer_config(lyr,"create")
        if lyr_config == None:
            return

        ##create edit session
        #desc = arcpy.Describe(lyr)
        #workspace = desc.path
        #with arcpy.da.Editor(workspace) as edit:
            #edit.startEditing(False, True)
            #edit.startOperation()
            #run update cursor
        cnt = 1
        if self.commontools.is_desktop == True:
            #desktop so give user progress dialog.  Have to declare as 'with'
            ProgressTool = pythonaddins.ProgressDialog
            ##get number of records to process for used with timing dialog
            selcount = len(lyr.getSelectionSet())

        else:
            #not desktop so give use dummy progress dialog.
            ProgressTool = DummyProgressDialog()
            
        with ProgressTool as dialog:
            if self.commontools.is_desktop:
                dialog.title = "Assetic Integration"
                dialog.description = "Creating Assets for layer {0}.".format(
                lyr.name)
                dialog.canCancel = False

            # Create update cursor for feature class 
            with arcpy.da.UpdateCursor(lyr, fields) as cursor:
                for row in cursor:
                    if self.commontools.is_desktop:
                        dialog.progress = cnt/selcount*100
                    if self._new_asset(row,lyr_config,fields):
                        cursor.updateRow(row)
                        iPass = iPass + 1
                    else:
                        iFail = iFail + 1
                    cnt = cnt + 1
##        else:
##            #no progress dialog as batch mode
##            # Create update cursor for feature class 
##            with arcpy.da.UpdateCursor(lyr, fields) as cursor:
##                for row in cursor:
##                    if self.new_asset(row,lyr_config,fields):
##                        cursor.updateRow(row)
##                        iPass = iPass + 1
##                    else:
##                        iFail = iFail + 1
                      
        message = "Finished {0} Asset Creation, {1} Assets created".format(
            lyr.name,str(iPass))
        if iFail > 0:
            message = message + ", {0} assets could not be created".format(str(iFail))
        self.commontools.new_message(message)

    def update_assets(self,lyr):
        """
        For the given layer create update assets for the selected features only if
        features have an assetic guid.
        :param lyr: is the layer to process (not layer name but ArcMap layer)
        """
        # Script Variables
        iPass = 0
        iFail = 0

        assetapi = assetic.AssetTools(self.asseticsdk.client)

        ##get layer configuration from xml file
        lyr_config,fields = self.get_layer_config(lyr,"update")
        if lyr_config == None:
            return

        #alias core fields for readability
        corefields = lyr_config["corefields"]

        cnt = 1        
        if self.commontools.is_desktop == True:
            #desktop so give user progress dialog.  Have to declare as 'with'
            ProgressTool = pythonaddins.ProgressDialog
            ##get number of records to process for use with timing dialog
            selcount = len(lyr.getSelectionSet())
        else:
            #not desktop so give use dummy progress dialog.
            ProgressTool = DummyProgressDialog()
        with ProgressTool as dialog:
            if self.commontools.is_desktop:
                dialog.title = "Assetic Integration"
                dialog.description = "Updating assets for layer {0}".format(
                    lyr.name)
                dialog.canCancel = False 
            # Create update cursor for feature class 
            with arcpy.da.UpdateCursor(lyr, fields) as cursor:
                for row in cursor:
                    if ("id" in corefields and \
                    row[fields.index(corefields["id"])] != None and \
                    row[fields.index(corefields["id"])].strip() != "") or\
                    ("asset_id" in corefields and \
                    row[fields.index(corefields["asset_id"])] != None and \
                    row[fields.index(corefields["asset_id"])].strip() != ""):
                        if self.commontools.is_desktop:
                            dialog.progress = cnt/selcount*100
                        ##create instance of asset object
                        asset = assetic.Assetic3IntegrationRepresentationsComplexAssetRepresentation()
                        asset.asset_category = lyr_config["asset_category"]
                        ##apply the values from arcMap to the core fields
                        for k,v in six.iteritems(corefields):
                            if k in asset.to_dict() and v in fields:
                                setattr(asset,k,row[fields.index(v)])
                        attributes = {}
                        if "attributefields" in lyr_config:
                            for k,v in six.iteritems(lyr_config["attributefields"]):
                                if k in asset.to_dict() and v in fields:
                                    attributes[k] = row[fields.index(v)]
                        asset.attributes = attributes
                        ##now execute the update
                        try:
                            response = assetapi.update_complex_asset(asset)
                        except assetic.rest.ApiException as e:
                            msg = "Error updating asset {0} {1} Status:{2},Reason:{3} {4}".format(
                                asset.asset_id,asset.id,e.status,e.reason,e.body)
                            asseticsdk.logger.error(msg)
                            self.commontools.new_message("Error Updating Asset:")
                            iFail = iFail + 1
                        else:
                            iPass = iPass + 1
                        cnt = cnt + 1
                           
        message = "Finished {0} Asset Update, {1} assets updated".format(
            lyr.name,str(iPass))
        if iFail > 0:
            message = "{0}, {1} assets not updated".format(
                message,str(iFail))
        self.commontools.new_message(message,"Assetic Integration")

    def display_asset(self,lyr):
        """
        Open assetic and display the first selected feature in layer
        :param lyr: The layer find selected assets.  Not layer name,layer object
        """
        ##get layer config details
        lyr_config,fields = self.get_layer_config(lyr,"create")
        if lyr_config == None:
            return
        
        assetid = None        
        idfield = None
        if "id" in lyr_config["corefields"]:
            idfield = lyr_config["corefields"]["id"]
        else:
            if "asset_id" in lyr_config["corefields"]:
                idfield = lyr_config["corefields"]["asset_id"]
            else:
                msg = "Asset ID and/or Asset GUID field must be defined for"\
                      "layer {0}".format(lyr.name)
                self.commontools.new_message(msg)
                self.asseticsdk.logger.warning(msg)
                return
        self.asseticsdk.logger.debug("Layer: {0}, id field: {1}".format(
            lyr.name,idfield))
        try:
            features = arcpy.da.SearchCursor(lyr,idfield)
            row = features.next()
            assetid = str(row[0])
        except Exception as ex:
            msg = "Unexpected Error Encountered, check log file"
            self.commontools.new_message(msg)            
            self.asseticsdk.logger.error(str(ex))
            return
        if assetid == None or assetid.strip() == "":
            msg = "Asset ID or Asset GUID is NULL.\nUnable to display asset"
            self.commontools.new_message(msg)
            self.asseticsdk.logger.warning(str(ex))
            return
        self.asseticsdk.logger.debug("Selected Asset to display: [{0}]".format(
            assetid))
        #Now launch Assetic
        apihelper = assetic.APIHelper(self.asseticsdk.client)
        apihelper.launch_assetic_asset(assetid)

    def _new_asset(self,row,lyr_config,fields):
        """
        Create a new asset for the given search result row
        :param row: a layer search result row, to create the asset for
        :param lyr_config: configuration object for asset field mapping
        :param fields: list of attribute fields
        :returns: Boolean True if success, else False
        """
        #instantiate assetic.AssetTools
        assettools = assetic.AssetTools(self.asseticsdk.client)
        
        ##instantiate the complete asset representation
        complete_asset_obj = assetic.AssetToolsCompleteAssetRepresentation()

        #create an instance of the complex asset object
        asset = assetic.Assetic3IntegrationRepresentationsComplexAssetRepresentation()

        ##set status (mandatory field)
        asset.status = "Active"
        
        ##set values from arcmap attribute table row from query
        asset.asset_category = lyr_config["asset_category"]

        #alias core fields for readability
        corefields = lyr_config["corefields"]
        
        ##set core field values from arcmap
        for k,v in six.iteritems(corefields):
            if k in asset.to_dict() and v in fields and \
            row[fields.index(v)] != None and \
            str(row[fields.index(v)]).strip() != "":
                setattr(asset,k,row[fields.index(v)])
        ##set core field values from defaults
        for k,v in six.iteritems(lyr_config["coredefaults"]):
            if k in asset.to_dict() and str(v).strip() != "":
                setattr(asset,k,v)

        ##Now we have core fields verify it actually needs to be created
        newasset = False
        if "id" in corefields:
            ##guid field set in ArcMap, use id as test
            if asset.id == None or asset.id.strip() == "":
               newasset = True
        else:
            ##guid not used, assume asset id is indicator
            if asset.asset_id == None or asset.asset_id.strip() == "":
               newasset = True
            else:
                ##test assetic for the asset id.  Perhaps user is not using guid
                ##and is manually assigning asset id.
                chk = assettools.get_asset(asset.asset_id)
                if chk == None:
                    newasset = True
        if newasset == False:
            msg = "Asset not created becuase it already has the following "\
                  "values: Asset ID={0},Asset GUID={1}".format(
                      asset.asset_id,asset.id)
            self.asseticsdk.logger.debug(msg)
            return False

        #It's a new asset...
        attributes = {}
        ##set attributes values from arcmap
        if "attributefields" in lyr_config:
            for k,v in six.iteritems(lyr_config["attributefields"]):
                if v in fields and row[fields.index(v)] != None and \
                str(row[fields.index(v)]).strip() != "":
                    attributes[k] = row[fields.index(v)]
        ##set attribute values from defaults
        for k,v in six.iteritems(lyr_config["attributedefaults"]):
            if str(v).strip() != "":
                attributes[k] = v
        #add the attributes to the asset and the asset to the complete object
        asset.attributes = attributes
        complete_asset_obj.asset_representation = asset

        #Create new asset
        response = assettools.create_complete_asset(
            complete_asset_obj)
        if response is None:
            msg = "Asset Not Created - Check log"
            self.commontools.new_message(msg)
            return False
        ##apply asset guid and/or assetid
        if "id" in corefields:
            row[fields.index(corefields["id"])] = \
                response.asset_representation.id
        if "asset_id" in corefields:
            row[fields.index(corefields["asset_id"])] = \
                response.asset_representation.asset_id
        ##Now update assetic with spatial data (TODO need API)
        geometry = row[fields.index('SHAPE@')]
        wkt = self.get_geom_wkt(4326,geometry)

        return True

    def get_geom_wkt(self,outsrid,geometry):
        """
        Get the well known text for a geometry in 4326 projection
        :rparam outsrid: The projection EPSG code to export WKT as (integer)
        :param geometry: The input geometry
        :returns: wkt string of geometry in the specified projection
        """
        tosr = arcpy.SpatialReference(outsrid)
        new_geom = geometry.projectAs(tosr)
        wkt = new_geom.WKT
        return wkt
