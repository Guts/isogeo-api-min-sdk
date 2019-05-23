# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - API Routes for Licenses (= CGUs, conditions) entities

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
from isogeo_pysdk.models import License
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
class ApiLicense:
    """Routes as methods of Isogeo API used to manipulate licenses (conditions).
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
        super(ApiLicense, self).__init__()

    @ApiDecorators._check_bearer_validity
    def licenses(
        self,
        workgroup_id: str = None,
        include: list = ["_abilities", "count"],
        caching: bool = 1,
    ) -> list:
        """Get workgroup licenses.

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
        url_licenses = utils.get_request_base_url(
            route="groups/{}/licenses".format(workgroup_id)
        )

        # request
        req_wg_licenses = self.api_client.get(
            url_licenses,
            headers=self.api_client.header,
            params=payload,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_wg_licenses)
        if isinstance(req_check, tuple):
            return req_check

        wg_licenses = req_wg_licenses.json()

        # if caching use or store the workgroup licenses
        if caching and not self.api_client._wg_licenses_names:
            self.api_client._wg_licenses_names = {
                i.get("name"): i.get("_id") for i in wg_licenses
            }

        # end of method
        return wg_licenses

    @ApiDecorators._check_bearer_validity
    def license(self, license_id: str) -> License:
        """Get details about a specific license.

        :param str license_id: license UUID
        """
        # check license UUID
        if not checker.check_is_uuid(license_id):
            raise ValueError("License ID is not a correct UUID.")
        else:
            pass

        # license route
        url_license = utils.get_request_base_url(route="licenses/{}".format(license_id))

        # request
        req_license = self.api_client.get(
            url_license,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_license)
        if isinstance(req_check, tuple):
            return req_check

        # end of method
        return License(**req_license.json())

    @ApiDecorators._check_bearer_validity
    def license_create(
        self, workgroup_id: str, check_exists: int = 1, license: object = License()
    ) -> License:
        """Add a new license to a workgroup.

        :param str workgroup_id: identifier of the owner workgroup
        :param int check_exists: check if a license already exists inot the workgroup:

        - 0 = no check
        - 1 = compare name [DEFAULT]

        :param class license: License model object to create
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError("Workgroup ID is not a correct UUID.")
        else:
            pass

        # check if license already exists in workgroup
        if check_exists == 1:
            # retrieve workgroup licenses
            if not self.api_client._wg_licenses_names:
                self.licenses(workgroup_id=workgroup_id, include=[])
            # check
            if license.name in self.api_client._wg_licenses_names:
                logger.debug(
                    "License with the same name already exists: {}. Use 'license_update' instead.".format(
                        license.name
                    )
                )
                return False
        else:
            pass

        # build request url
        url_license_create = utils.get_request_base_url(
            route="groups/{}/licenses".format(workgroup_id)
        )

        # request
        req_new_license = self.api_client.post(
            url_license_create,
            data=license.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_license)
        if isinstance(req_check, tuple):
            return req_check

        # load new license and save it to the cache
        new_license = License(**req_new_license.json())
        self.api_client._wg_licenses_names[new_license.name] = new_license._id

        # end of method
        return new_license

    @ApiDecorators._check_bearer_validity
    def delete(self, workgroup_id: str, license_id: str):
        """Delete a license from Isogeo database.

        :param str workgroup_id: identifier of the owner workgroup
        :param str license_id: identifier of the resource to delete
        """
        # check workgroup UUID
        if not checker.check_is_uuid(workgroup_id):
            raise ValueError(
                "Workgroup ID is not a correct UUID: {}".format(workgroup_id)
            )
        else:
            pass

        # check license UUID
        if not checker.check_is_uuid(license_id):
            raise ValueError("License ID is not a correct UUID: {}".format(license_id))
        else:
            pass

        # request URL
        url_license_delete = utils.get_request_base_url(
            route="groups/{}/licenses/{}".format(workgroup_id, license_id)
        )

        # request
        req_license_deletion = self.api_client.delete(
            url_license_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_license_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_license_deletion

    @ApiDecorators._check_bearer_validity
    def license_exists(self, license_id: str) -> bool:
        """Check if the specified license exists and is available for the authenticated user.

        :param str license_id: identifier of the license to verify
        """
        # check license UUID
        if not checker.check_is_uuid(license_id):
            raise ValueError("License ID is not a correct UUID: {}".format(license_id))
        else:
            pass

        # URL builder
        url_license_exists = "{}{}".format(
            utils.get_request_base_url("licenses"), license_id
        )

        # request
        req_license_exists = self.api_client.get(
            url_license_exists,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_license_exists)
        if isinstance(req_check, tuple):
            return req_check

        return req_license_exists

    @ApiDecorators._check_bearer_validity
    def license_update(self, license: License, caching: bool = 1) -> License:
        """Update a license owned by a workgroup.

        :param class license: License model object to update
        :param bool caching: option to cache the response
        """
        # check license UUID
        if not checker.check_is_uuid(license._id):
            raise ValueError("License ID is not a correct UUID: {}".format(license._id))
        else:
            pass

        # URL
        url_license_update = utils.get_request_base_url(
            route="groups/{}/licenses/{}".format(license.owner.get("_id"), license._id)
        )

        # request
        req_license_update = self.api_client.put(
            url=url_license_update,
            data=license.to_dict(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_license_update)
        if isinstance(req_check, tuple):
            return req_check

        # update license in cache
        new_license = License(**req_license_update.json())
        if caching:
            self.api_client._wg_licenses_names[new_license.name] = new_license._id

        # end of method
        return new_license


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_license = ApiLicense()
