# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Catalogs entities

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
from isogeo_pysdk.models import Catalog
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
class ApiCatalog:
    """Routes as methods of Isogeo API used to manipulate catalogs (conditions).
    """

    def __init__(self, api_client=None):
        if api_client is not None:
            self.api_client = api_client

        # store API client (Request [Oauthlib] Session) and pass it to the decorators
        self.api_client = api_client
        ApiDecorators.api_client = api_client

        # ensure platform and others params to request
        self.platform, self.api_url, self.app_url, self.csw_url, self.mng_url, self.oc_url, self.ssl = utils.set_base_url(
            self.api_client.platform
        )
        # initialize
        super(ApiCatalog, self).__init__()

    @ApiDecorators._check_bearer_validity
    def catalogs(
        self,
        workgroup_id: str = None,
        include: list = ["_abilities", "count"],
        caching: bool = 1,
    ) -> list:
        """Get workgroup catalogs.

        :param str workgroup_id: identifier of the owner workgroup
        :param list include: additionnal subresource to include in the response
        :param bool caching: option to cache the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # handling request parameters
        payload = {"_include": include}

        # request URL
        url_catalogs = utils.get_request_base_url(
            route="groups/{}/catalogs".format(workgroup_id)
        )

        # request
        req_wg_catalogs = self.api_client.get(
            url_catalogs,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_wg_catalogs)
        if isinstance(req_check, tuple):
            return req_check

        wg_catalogs = req_wg_catalogs.json()

        # if caching use or store the workgroup catalogs
        if caching and not self.api_client._wg_catalogs_names:
            self.api_client._wg_catalogs_names = {
                i.get("name"): i.get("_id") for i in wg_catalogs
            }

        # end of method
        return wg_catalogs

    @ApiDecorators._check_bearer_validity
    def catalog(
        self,
        workgroup_id: str,
        catalog_id: str,
        include: list = ["_abilities", "count"],
    ) -> Catalog:
        """Get details about a specific catalog.

        :param str workgroup_id: identifier of the owner workgroup
        :param str catalog_id: catalog UUID
        :param list include: additionnal subresource to include in the response
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass
        # check catalog UUID
        if not checker.check_is_uuid(catalog_id):
            raise ValueError("Catalog ID is not a correct UUID.")
        else:
            pass

        # request parameter
        payload = {"_include": include}

        # catalog route
        url_catalog = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog_id)
        )

        # request
        req_catalog = self.api_client.get(
            url=url_catalog,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_catalog)
        if isinstance(req_check, tuple):
            return req_check

        # handle bad JSON attribute
        catalog = req_catalog.json()
        catalog["scan"] = catalog.pop("$scan")

        # end of method
        return Catalog(**catalog)

    @ApiDecorators._check_bearer_validity
    def create(
        self, workgroup_id: str, check_exists: int = 1, catalog: object = Catalog()
    ) -> Catalog:
        """Add a new catalog to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a catalog already exists inot the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]

        :param class catalog: Catalog model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if catalog already exists in workgroup
        if check_exists == 1:
            # retrieve workgroup catalogs
            if not self.api_client._wg_catalogs_names:
                self.catalogs(workgroup_id=workgroup_id, include=[])
            # check
            if catalog.name in self.api_client._wg_catalogs_names:
                logger.debug(
                    "Catalog with the same name already exists: {}. Use 'catalog_update' instead.".format(
                        catalog.name
                    )
                )
                return False
        else:
            pass

        # build request url
        url_catalog_create = utils.get_request_base_url(
            route="groups/{}/catalogs".format(workgroup_id)
        )

        # request
        req_new_catalog = self.api_client.post(
            url_catalog_create,
            data=catalog.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_catalog)
        if isinstance(req_check, tuple):
            return req_check

        # handle bad JSON attribute
        new_catalog = req_new_catalog.json()
        new_catalog["scan"] = new_catalog.pop("$scan")

        # load new catalog and save it to the cache
        new_catalog = Catalog(**new_catalog)
        self.api_client._wg_catalogs_names[new_catalog.name] = new_catalog._id

        # end of method
        return new_catalog

    @ApiDecorators._check_bearer_validity
    def delete(self, workgroup_id: str, catalog_id: str):
        """Delete a catalog from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str catalog_id: identifier of the resource to delete
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check catalog UUID
        if not checker.check_is_uuid(catalog_id):
            raise ValueError("Catalog ID is not a correct UUID: {}".format(catalog_id))
        else:
            pass

        # request URL
        url_catalog_delete = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog_id)
        )

        # request
        req_catalog_deletion = self.api_client.delete(
            url_catalog_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_catalog_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_catalog_deletion

    @ApiDecorators._check_bearer_validity
    def exists(self, workgroup_id: str, catalog_id: str) -> bool:
        """Check if the specified catalog exists and is available for the authenticated user.

        :param str workgroup_id: identifier of the owner workgroup
        :param str catalog_id: identifier of the catalog to verify
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass
        # check catalog UUID
        if not checker.check_is_uuid(catalog_id):
            raise ValueError("Catalog ID is not a correct UUID: {}".format(catalog_id))
        else:
            pass

        # URL builder
        url_catalog_exists = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(workgroup_id, catalog_id)
        )

        # request
        req_catalog_exists = self.api_client.get(
            url=url_catalog_exists,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_catalog_exists)
        if isinstance(req_check, tuple):
            return req_check

        return req_catalog_exists

    @ApiDecorators._check_bearer_validity
    def update(self, catalog: Catalog, caching: bool = 1) -> Catalog:
        """Update a catalog owned by a workgroup.

        :param class catalog: Catalog model object to update
        :param bool caching: option to cache the response
        """
        # check catalog UUID
        if not checker.check_is_uuid(catalog._id):
            raise ValueError("Catalog ID is not a correct UUID: {}".format(catalog._id))
        else:
            pass

        # URL
        url_catalog_update = utils.get_request_base_url(
            route="groups/{}/catalogs/{}".format(catalog.owner.get("_id"), catalog._id)
        )

        # request
        req_catalog_update = self.api_client.put(
            url=url_catalog_update,
            json=catalog.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_catalog_update)
        if isinstance(req_check, tuple):
            return req_check

        # handle bad JSON attribute
        new_catalog = req_catalog_update.json()
        new_catalog["scan"] = new_catalog.pop("$scan")

        # load new catalog and save it to the cache
        new_catalog = Catalog(**new_catalog)
        if caching:
            self.api_client._wg_catalogs_names[new_catalog.name] = new_catalog._id

        # end of method
        return new_catalog


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_catalog = ApiCatalog()