# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes to manage metadata links.

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
import logging

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.models import Link, Metadata
from isogeo_pysdk.utils import IsogeoUtils

# #############################################################################
# ########## Global #############
# ##################################

logger = logging.getLogger(__name__)
checker = IsogeoChecker()
utils = IsogeoUtils()


# #############################################################################
# ########## Classes ###############
# ##################################
class ApiLink:
    """Routes as methods of Isogeo API used to manipulate metadata links (CGUs).
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [oAuthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform and others params to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )
        # initialize
        super(ApiLink, self).__init__()

    @ApiDecorators._check_bearer_validity
    def listing(self, metadata: Metadata) -> list:
        """Get links of a metadata.

        :param Metadata metadata: metadata (resource)
        """
        # request URL
        url_links = utils.get_request_base_url(
            route="resources/{}/links/".format(metadata._id)
        )

        # request
        req_links = self.api_client.get(
            url=url_links,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_links)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_links.json()

    # -- Routes to manage the related objects ------------------------------------------
    @ApiDecorators._check_bearer_validity
    def kinds_actions(self) -> list:
        """Get the relation between kinds and action for links."""
        # request URL
        url_links = utils.get_request_base_url(route="link-kinds/")

        # request
        req_links = self.api_client.get(
            url=url_links,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_links)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return req_links.json()


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_test = ApiLink()
