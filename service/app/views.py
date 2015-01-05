from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPInternalServerError,
    HTTPForbidden,
    HTTPUnauthorized
)

import logging
log = logging.getLogger(__name__)

import os
import sys
import time
from datetime import datetime
from lxml import etree, html

from config import Config

from Helpers import *
from Network import Network

from config import Config

@view_config(route_name='health-check', request_method='GET', renderer='string')
def health_check(request):
    """
    Show the health check view.
    """
    log.info("GET {0} - {1} - {2}".format(request.path, request.remote_addr, request.user_agent))

    # is mongo ok?
    try:
        db = mdb(request)
        doc =  db.health_check.find_one()
        return 'OK'
    except:
        raise HTTPInternalServerError


@view_config(route_name='home', request_method='GET', renderer='json')
def home_page(request):
    claims, sites = verify_access(request)
    return { 'sites': sites }

@view_config(route_name='network-build', request_method='GET', renderer='json')
def network_build(request):
    """For a given site - assemble the entity graph
    
    @params:
    request.matchdict: code, the site of interest
    """
    site = request.matchdict['code']
    claims, site = verify_access(request, site=site)

    n = Network(request)
    n.build()

    return { 'started': True, 'name': site['name'], 'url': site['url'] }


@view_config(route_name="network-stats", request_method='GET', renderer='json')
def network_stats(request):
    site = request.matchdict['code']
    claims, site = verify_access(request, site=site)

    n = Network(request)
    degree = n.calculate_average_degree()
    d = [ d[1] * 100 for d in degree.items() ]

    return {
        'name': n.name,
        'url': n.url,
        'degree': sum(d) / len(d)
    }

@view_config(route_name='build-status', request_method='GET', renderer='json')
def build_status(request):

    db = mdb(request)
    site = request.matchdict['code']
    graph_type = request.matchdict['explore']

    doc = db.network.find_one({ 'site': site, 'graph_type': graph_type })
    if doc is not None:
        claims = verify_access(request)
        graph_data = doc['graph_data']
        doc = db.progress.remove({ 'site': site })
        return { 'total': None, 'processed': None, 'graph': graph_data }
    else:
        doc = db.progress.find_one({ 'site': site })
        return { 'total': doc['total'], 'processed': doc['processed'] }

def bare_tag(tag):
    return tag.rsplit("}", 1)[-1]


