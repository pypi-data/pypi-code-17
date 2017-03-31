#!/usr/bin/env python
'''
Central execution points for non-python services
'''

import logging

from neo4j.v1 import GraphDatabase, basic_auth
import neo4j.bolt.connection

import elasticsearch.exceptions

from isoprene_pumpjack.constants.environment import environment
from isoprene_pumpjack.utils.neo_to_d3 import neo_to_d3
from isoprene_pumpjack.exceptions import IsopumpException

logger = logging.getLogger(__name__)

def execute_cypher(cypher_statement):
    '''Configure and safely execute a cypher statement'''

    logger.debug("Executing cypher statement")
    try:
        bolt_driver = GraphDatabase.driver(
            environment["ISOPRENE_PUMPJACK_BOLT_URL"],
            auth=basic_auth(
                environment["ISOPRENE_PUMPJACK_BOLT_USER"],
                environment["ISOPRENE_PUMPJACK_BOLT_PASSWORD"]
            )
        )
        with bolt_driver.session() as session:
            result = session.run(cypher_statement)
    except neo4j.bolt.connection.ServiceUnavailable as e:
        logger.error(e)
        raise IsopumpException("Could not reach graph server", status_code=503, payload={
            "message_original": e.message
        })
    return result

def execute_cypher_get_d3(cypher_statement, nodeLabels=[], linkLabels=[]):
    '''In addition to safe execution, return the cypher query in d3 dict format'''
    logger.debug("Executing cypher and returning as d3 dict")
    result = execute_cypher(cypher_statement)
    data = neo_to_d3(result, nodeLabels, linkLabels)
    return data

def execute_search(elasticsearch_dsl_search_object):
    '''Execute an elasticsearch-dsl object safely'''
    try:
        response = elasticsearch_dsl_search_object.execute()
    except elasticsearch.exceptions.ConnectionError as e:
        logger.error(e)
        raise IsopumpException("Could not reach document server", status_code=503)
    return response
