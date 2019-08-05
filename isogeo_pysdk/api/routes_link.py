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
import re

# 3rd party
from requests.models import Response

# submodules
from isogeo_pysdk.checker import IsogeoChecker
from isogeo_pysdk.decorators import ApiDecorators
from isogeo_pysdk.enums import LinkActions, LinkKinds, LinkTypes
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

    @ApiDecorators._check_bearer_validity
    def get(self, metadata_id: str, link_id: str) -> Link:
        """Get details about a specific link.

        :param str metadata_id: metadata UUID
        :param str link_id: link UUID

        :rtype: Link

        :Example:

        .. code-block:: python

            # get a metadata
            md = isogeo.metadata.get(METADATA_UUID)
            # list its links
            md_links = isogeo.metadata.links.listing(md)
            # get the first link
            link = isogeo.metadata.links.get(
                metadata_id=md._id,
                link_id=md_links[0].get("_id")
                )
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata_id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata_id)
            )
        else:
            pass

        # check link UUID
        if not checker.check_is_uuid(link_id):
            raise ValueError("Features Attribute ID is not a correct UUID.")
        else:
            pass

        # URL
        url_link = utils.get_request_base_url(
            route="resources/{}/links/{}".format(metadata_id, link_id)
        )

        # request
        req_link = self.api_client.get(
            url=url_link,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_link)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        link_augmented = req_link.json()
        link_augmented["parent_resource"] = metadata_id

        # end of method
        return Link(**link_augmented)

    @ApiDecorators._check_bearer_validity
    def create(self, metadata: Metadata, link: Link) -> Link:
        """Add a new link to a metadata (= resource).

        :param Metadata metadata: metadata (resource) to edit
        :param Link link: link object to create

        :returns: 409 if a link with the same name already exists.

        :rtype: Link or tuple

        :Example:

        .. code-block:: python

            # retrieve metadata
            md = isogeo.metadata.get(METADATA_UUID)
            # create the link locally
            new_link = Link(
                type="url",
                restriction="patent",
                description="Do not use for commercial purpose.",
                )
            # add it to the metadata
            isogeo.metadata.links.create(md, new_link)
        """
        # check metadata UUID
        if not checker.check_is_uuid(metadata._id):
            raise ValueError(
                "Metadata ID is not a correct UUID: {}".format(metadata._id)
            )
        else:
            pass

        # check link actions, kinds and types
        if not all(i in LinkActions.__members__ for i in link.actions):
            raise ValueError(
                "Link action '{}' are not an accepted value. Accepted values: {}".format(
                    link.actions, " | ".join([e.name for e in LinkActions])
                )
            )
        else:
            pass

        if link.kind not in LinkKinds.__members__:
            raise ValueError(
                "Link kind '{}' is not an accepted value. Accepted values: {}".format(
                    link.kind, " | ".join([e.name for e in LinkKinds])
                )
            )
        else:
            pass

        if link.type not in LinkTypes.__members__:
            raise ValueError(
                "Link type '{}' is not an accepted value. Accepted values: {}".format(
                    link.type, " | ".join([e.name for e in LinkTypes])
                )
            )
        else:
            pass

        # check relation between link kind/actions
        link.actions = self.clean_kind_action_liability(
            link_actions=link.actions, link_kind=link.kind
        )

        # deprecation warnings
        if link.kind in (
            "esriFeatureService",
            "esriMapService",
            "esriTileService",
            "wfs",
            "wms",
            "wmts",
        ):
            logger.warning(
                DeprecationWarning(
                    "Creation of geographic services with raw URL links is deprecated. "
                    "Use services layers instead."
                )
            )

        # URL
        url_link_create = utils.get_request_base_url(
            route="resources/{}/links".format(metadata._id)
        )

        # request
        req_new_link = self.api_client.post(
            url=url_link_create,
            json=link.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_new_link)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        link_augmented = req_new_link.json()
        link_augmented["parent_resource"] = metadata._id

        # end of method
        return Link(**link_augmented)

    @ApiDecorators._check_bearer_validity
    def delete(self, link: Link, metadata: Metadata = None) -> Response:
        """Delete a link from a metadata.

        :param Link link: Link model object to delete
        :param Metadata metadata: parent metadata (resource) containing the link. Optional if the link contains the 'parent_resource' attribute.

        :rtype: Response

        """
        # check link UUID
        if not checker.check_is_uuid(link._id):
            raise ValueError("Link ID is not a correct UUID: {}".format(link._id))
        else:
            pass

        # retrieve parent metadata
        if not checker.check_is_uuid(link.parent_resource) and not metadata:
            raise ValueError("Link parent metadata is required. Requesting it...")
        elif not checker.check_is_uuid(link.parent_resource) and metadata:
            link.parent_resource = metadata._id
        else:
            pass

        # URL
        url_link_delete = utils.get_request_base_url(
            route="resources/{}/links/{}".format(link.parent_resource, link._id)
        )

        # request
        req_link_deletion = self.api_client.delete(
            url=url_link_delete,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_link_deletion)
        if isinstance(req_check, tuple):
            return req_check

        return req_link_deletion

    @ApiDecorators._check_bearer_validity
    def update(self, link: Link, metadata: Metadata = None) -> Link:
        """Update a link.
        
        :param Link link: Link model object to update
        :param Metadata metadata: parent metadata (resource) containing the link. Optional if the link contains the 'parent_resource' attribute.
        """
        # check link UUID
        if not checker.check_is_uuid(link._id):
            raise ValueError("Link ID is not a correct UUID: {}".format(link._id))
        else:
            pass

        # retrieve parent metadata
        if not checker.check_is_uuid(link.parent_resource) and not metadata:
            raise ValueError("Link parent metadata is required. Requesting it...")
        elif not checker.check_is_uuid(link.parent_resource) and metadata:
            link.parent_resource = metadata._id
        else:
            pass

        # URL
        url_link_update = utils.get_request_base_url(
            route="resources/{}/links/{}".format(link.parent_resource, link._id)
        )

        # request
        req_link_update = self.api_client.put(
            url=url_link_update,
            json=link.to_dict_creation(),
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            verify=self.api_client.ssl,
            timeout=self.api_client.timeout,
        )

        # checking response
        req_check = checker.check_api_response(req_link_update)
        if isinstance(req_check, tuple):
            return req_check

        # add parent resource id to keep tracking
        link_augmented = req_link_update.json()
        link_augmented["parent_resource"] = link.parent_resource

        # end of method
        return Link(**link_augmented)

    # -- Routes to manage the related objects ------------------------------------------
    @ApiDecorators._check_bearer_validity
    def download_hosted(self, link: Link, encode_clean: bool = 1) -> tuple:
        """Download hosted resource.

        :param Link link: link object
        :param bool encode_clean: option to ensure a clean filename and avoid OS errors

        :returns: tuple(stream, filename, human readable size)
        :rtype: tuple


        Example of resource_link dict:

        .. code-block:: python

            # get links from a metadata
            md_links = isogeo.metadata.links.listing(Metadata(_id=METADATA_UUID))
            # filter on hosted links
            hosted_links = [
                link for link in md_links
                if link.get("type") == "hosted"
                ]
            # get the stream, the filename and the size (in human readable format)
            dl_stream = isogeo.metadata.links.download_hosted(Link(**hosted_links[0]))
            # download the file and store it locally
            with open("./" + dl_stream[1], "wb") as fd:
                for block in dl_stream[0].iter_content(1024):
                    fd.write(block)

        """
        # check resource link type
        if link.type != "hosted":
            raise ValueError(
                "Resource link passed is not a hosted one: {}".format(link.type("type"))
            )
        else:
            pass

        # request URL
        url_download_hosted = utils.get_request_base_url(route=link.url)

        # request
        req_download_hosted = self.api_client.get(
            url=url_download_hosted,
            headers=self.api_client.header,
            proxies=self.api_client.proxies,
            stream=True,
            timeout=self.api_client.timeout,
            verify=self.api_client.ssl,
        )

        # checking response
        req_check = checker.check_api_response(req_download_hosted)
        if isinstance(req_check, tuple):
            return req_check

        # get filename from header
        content_disposition = req_download_hosted.headers.get("Content-Disposition")
        if content_disposition:
            filename = re.findall("filename=(.+)", content_disposition)[0]
        else:
            filename = link.title

        # remove special characters
        if encode_clean:
            filename = utils.encoded_words_to_text(filename)
            filename = re.sub(r"[^\w\-_\. ]", "", filename)

        # end of method
        return (req_download_hosted, filename, utils._convert_octets(link.size))

    @ApiDecorators._check_bearer_validity
    def kinds_actions(self, caching: bool = 1) -> list:
        """Get the relation between kinds and action for links.

        :param bool caching: cache the response into the main API client instance. Defaults to True.

        :rtype: list
        """
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

        # caching
        if caching:
            self.api_client._links_kinds_actions = req_links.json()

        # end of method
        return req_links.json()

    # -- Helpers -----------------------------------------------------------------------
    def clean_kind_action_liability(self, link_actions: list, link_kind: str) -> list:
        """Link available actions depend on link kind.\
            Relationships between kinds and actions are described in the `/link-kinds` route.
            This is a helper checking the liability between kind/actions/type and cleaning if needed.
            Useful before creating or updating a link.

        :param list link_actions: link actions
        :param str link_kind: link kind

        :rtype: list
        """
        # get matrix kinds/actions as dict - use cache if exists
        if self.api_client._links_kinds_actions:
            matrix_kind_actions = {
                i.get("kind"): i.get("actions")
                for i in self.api_client._links_kinds_actions
            }
        else:
            matrix_kind_actions = {
                i.get("kind"): i.get("actions") for i in self.kinds_actions()
            }

        # compare with available actions
        if not all(i in matrix_kind_actions.get(link_kind) for i in link_actions):
            logger.warning(
                "Actions have been cleaned because only these actions '{}'"
                "can be set with this kind of link '{}'.".format(
                    " | ".join(matrix_kind_actions.get(link_kind)), link_kind
                )
            )
            link_actions = [
                action
                for action in link_actions
                if action in matrix_kind_actions.get(link_kind)
            ]

        return link_actions


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    api_test = ApiLink()
