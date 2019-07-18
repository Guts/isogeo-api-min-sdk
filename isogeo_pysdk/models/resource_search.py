# -*- coding: UTF-8 -*-
#! python3

"""
    Isogeo API v1 - Model of Resource search entity

    See: http://help.isogeo.com/api/complete/index.html#definition-search
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint

# other model
# from isogeo_pysdk.models.resource import Resource
# from isogeo_pysdk.models.tag import Tag

# #############################################################################
# ########## Classes ###############
# ##################################
class ResourceSearch(object):
    """Resource searchs are entities used to organize and shares metadata of a workgroup.

    ```json

    ```
    """

    """
    Attributes:
      attr_types (dict): basic structure of search attributes. {"attribute name": "attribute type"}.
    """
    attr_types = {
        "envelope": object,
        "limit": int,
        "offset": int,
        "query": str,
        "results": list,
        "tags": list,
        "total": int,
    }

    def __init__(
        self,
        envelope: dict = None,
        limit: int = None,
        offset: int = None,
        query: str = None,
        results: list = None,
        tags: list = None,
        total: int = None,
    ):
        """resource/search? model"""

        # default values for the object attributes/properties
        self._envelope = None
        self._limit = None
        self._offset = None
        self._query = None
        self._results = None
        self._tags = None
        self._total = None

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if envelope is not None:
            self._envelope = envelope
        if limit is not None:
            self._limit = limit
        if offset is not None:
            self._offset = offset
        if query is not None:
            self._query = query
        if results is not None:
            self._results = results
        if tags is not None:
            self._tags = tags
        if total is not None:
            self._total = total

    # -- PROPERTIES --------------------------------------------------------------------
    # search results envelope
    @property
    def envelope(self) -> dict:
        """Gets the abilities of this Resource search.

        :return: The abilities of this Resource search.
        :rtype: str
        """
        return self._envelope

    @envelope.setter
    def envelope(self, envelope: dict):
        """Sets the envelope of this InlineResponse2001.

        The aggregated convex hull for the entire serach results. Might be null (if the results span the entire globe, for instance).  # noqa: E501

        :param envelope: The envelope of this InlineResponse2001.  # noqa: E501
        :type: object
        """

        self._envelope = envelope

    # search creation date
    @property
    def limit(self) -> int:
        """Gets the created of this Resource search.

        :return: The created of this Resource search.
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit: int):
        """Sets the limit of this InlineResponse2001.


        :param int limit: The limit of this Resource Search
        """

        self._limit = limit

    # offset UUID
    @property
    def offset(self) -> str:
        """Gets the id of this Resource search.

        :return: The id of this Resource search.
        :rtype: str
        """
        return self._offset

    @offset.setter
    def offset(self, offset: str):
        """Sets the id of this Resource search.

        :param str id: The id of this Resource search.
        """

        self._offset = offset

    # search last modification date
    @property
    def query(self) -> str:
        """Gets the modified of this Resource search.

        :return: The modified of this Resource search.
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query: str):
        """Sets the query of this InlineResponse2001.


        :param query: The query of this InlineResponse2001.  # noqa: E501
        :type: object
        """

        self._query = query

    # search results tags
    @property
    def results(self) -> list:
        """Gets the tag of this Resource search.

        :return: The tag of this Resource search.
        :rtype: list
        """
        return self._results

    @results.setter
    def results(self, results: list):
        """Sets the results of this InlineResponse2001.


        :param results: The results of this InlineResponse2001.  # noqa: E501
        :type: list[Resource]
        """

        self._results = results

    # tags
    @property
    def tags(self) -> list:
        """Gets the tags of this Resource search.

        :return: The tags of this Resource search.
        :rtype: str
        """
        return self._tags

    @tags.setter
    def tags(self, tags: list):
        """Sets the tags of this InlineResponse2001.

        The aggregated set of tags for the entire search results  # noqa: E501

        :param tags: The tags of this InlineResponse2001.  # noqa: E501
        :type: Tags
        """

        self._tags = tags

    # total
    @property
    def total(self) -> int:
        """Gets the total of this Resource search.

        :return: The total of this Resource search.
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total: int):
        """Sets the total of this Resource search.

        :param int total: The total of this Resource search.
        """

        self._total = total

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.attr_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(ResourceSearch, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, ResourceSearch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal"""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """ standalone execution """
    search = ResourceSearch()