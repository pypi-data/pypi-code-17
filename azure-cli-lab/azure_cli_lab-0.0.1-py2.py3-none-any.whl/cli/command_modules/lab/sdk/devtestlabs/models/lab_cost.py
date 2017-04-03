# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# coding: utf-8
# pylint: skip-file
from msrest.serialization import Model


class LabCost(Model):
    """A cost item.

    :param target_cost: The target cost properties
    :type target_cost: :class:`TargetCostProperties
     <azure.mgmt.devtestlabs.models.TargetCostProperties>`
    :param lab_cost_summary: The lab cost summary component of the cost data.
    :type lab_cost_summary: :class:`LabCostSummaryProperties
     <azure.mgmt.devtestlabs.models.LabCostSummaryProperties>`
    :param lab_cost_details: The lab cost details component of the cost data.
    :type lab_cost_details: list of :class:`LabCostDetailsProperties
     <azure.mgmt.devtestlabs.models.LabCostDetailsProperties>`
    :param resource_costs: The resource cost component of the cost data.
    :type resource_costs: list of :class:`LabResourceCostProperties
     <azure.mgmt.devtestlabs.models.LabResourceCostProperties>`
    :param currency_code: The currency code of the cost.
    :type currency_code: str
    :param start_date_time: The start time of the cost data.
    :type start_date_time: datetime
    :param end_date_time: The end time of the cost data.
    :type end_date_time: datetime
    :param created_date: The creation date of the cost.
    :type created_date: datetime
    :param provisioning_state: The provisioning status of the resource.
    :type provisioning_state: str
    :param unique_identifier: The unique immutable identifier of a resource
     (Guid).
    :type unique_identifier: str
    :param id: The identifier of the resource.
    :type id: str
    :param name: The name of the resource.
    :type name: str
    :param type: The type of the resource.
    :type type: str
    :param location: The location of the resource.
    :type location: str
    :param tags: The tags of the resource.
    :type tags: dict
    """

    _attribute_map = {
        'target_cost': {'key': 'properties.targetCost', 'type': 'TargetCostProperties'},
        'lab_cost_summary': {'key': 'properties.labCostSummary', 'type': 'LabCostSummaryProperties'},
        'lab_cost_details': {'key': 'properties.labCostDetails', 'type': '[LabCostDetailsProperties]'},
        'resource_costs': {'key': 'properties.resourceCosts', 'type': '[LabResourceCostProperties]'},
        'currency_code': {'key': 'properties.currencyCode', 'type': 'str'},
        'start_date_time': {'key': 'properties.startDateTime', 'type': 'iso-8601'},
        'end_date_time': {'key': 'properties.endDateTime', 'type': 'iso-8601'},
        'created_date': {'key': 'properties.createdDate', 'type': 'iso-8601'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'unique_identifier': {'key': 'properties.uniqueIdentifier', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(self, target_cost=None, lab_cost_summary=None, lab_cost_details=None, resource_costs=None, currency_code=None, start_date_time=None, end_date_time=None, created_date=None, provisioning_state=None, unique_identifier=None, id=None, name=None, type=None, location=None, tags=None):
        self.target_cost = target_cost
        self.lab_cost_summary = lab_cost_summary
        self.lab_cost_details = lab_cost_details
        self.resource_costs = resource_costs
        self.currency_code = currency_code
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.created_date = created_date
        self.provisioning_state = provisioning_state
        self.unique_identifier = unique_identifier
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        self.tags = tags
