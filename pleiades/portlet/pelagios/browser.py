import logging
from random import choice
from urllib import urlencode

import httplib2
import simplejson

from Acquisition import aq_inner, aq_parent
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, Interface, Attribute
from zope.publisher.browser import BrowserPage, BrowserView

from Products.PleiadesEntity.content.interfaces import ILocation, IName, IPlace
from pleiades.portlet.pelagios import client

log = logging.getLogger("pleiades.portlet.pelagios")


class RelatedPelagiosJson(BrowserView):

    """Makes one Pelagios Flickr API call and writes data to be used in a
    portal template."""

    def __call__(self, **kw):
        data = {}
        context = self.context
        
        if IPlace.providedBy(context):
            pid = context.getId() # local id like "149492"
        elif ILocation.providedBy(context) or IName.providedBy(context):
            pid = aq_parent(aq_inner(context)).getId()
        else:
            pid = None

        if pid is not None:
            try:
                annotations = client.annotations(pid)
            except client.PelagiosAPIError, e:
                annotations = None
                log.exception("Pelagios API Error: %s", str(e))
        else:
            annotations = None

        data = dict(
            pid=pid,
            purl="http://pleiades.stoa.org/places/" + pid or ""
            datasets_home="http://pelagios.dme.ait.ac.at/api/datasets",
            annotations=annotations )
        
        self.request.response.setStatus(200)
        self.request.response.setHeader('Content-Type', 'application/json')
        return simplejson.dumps(data)

