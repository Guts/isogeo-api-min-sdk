# -*- coding: UTF-8 -*-
#! python3  # noqa E265

"""
    Isogeo API v1 - Model of FeatureAttributes entity

    See: http://help.isogeo.com/api/complete/index.html
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import pprint


# #############################################################################
# ########## Classes ###############
# ##################################
class FeatureAttribute(object):
    """FeatureAttributes are entities included as subresource into metadata.

    :param str _id: UUID, defaults to None
    :param str alias: alias of the feature attribute, defaults to None
    :param str dataType: kind of field (varchar, integer32...), defaults to None
    :param str description: description of the feature attribute, defaults to None
    :param str language: language of the description, defaults to None
    :param int length: length of the values accepted in the attribute, defaults to None
    :param str name: attribute name, defaults to None
    :param int precision: value precision, defaults to None
    :param int scale: scale of display, defaults to None

    :Example:

    .. code-block:: json

        {
            "_id": string (uuid),
            "alias": string,
            "dataType": string,
            "description": string,
            "language": string,
            "length": int,
            "name": string,
            "precision": int,
            "scale": int,
        }
    """

    attr_types = {
        "_id": str,
        "alias": str,
        "dataType": str,
        "description": str,
        "isAutoGenerated": bool,
        "isNullable": bool,
        "isReadOnly": bool,
        "hasElevation": bool,
        "hasMeasure": bool,
        "language": str,
        "length": int,
        "name": str,
        "precision": int,
        "propertyType": str,
        "scale": int,
        "spatialContext": str,
        # specific
        "parent_resource": str,
    }

    attr_crea = {
        "alias": str,
        "dataType": str,
        "description": str,
        "isAutoGenerated": bool,
        "isNullable": bool,
        "isReadOnly": bool,
        "hasElevation": bool,
        "hasMeasure": bool,
        "language": str,
        "length": int,
        "name": str,
        "precision": int,
        "propertyType": str,
        "scale": int,
        "spatialContext": str,
    }

    ATTR_MAP = {}

    def __init__(
        self,
        _id: str = None,
        alias: str = None,
        dataType: str = None,
        description: str = None,
        isAutoGenerated: bool = None,
        isNullable: bool = None,
        isReadOnly: bool = None,
        hasElevation: bool = None,
        hasMeasure: bool = None,
        language: str = None,
        length: int = None,
        name: str = None,
        precision: int = None,
        propertyType: str = None,
        scale: int = None,
        spatialContext: str = None,
        # specific to implementation (SDK)
        parent_resource: str = None,
    ):
        """Metadata Feature Attribute model."""

        # default values for the object attributes/properties
        self.__id = None
        self._alias = None
        self._dataType = None
        self._description = None
        self._language = None
        self._isAutoGenerated = None
        self._isNullable = None
        self._isReadOnly = None
        self._hasElevation = None
        self._hasMeasure = None
        self._length = None
        self._precision = None
        self._scale = None
        self._spatialContext = None
        self._name = None
        self._propertyType = None
        # additional parameters
        self.parent_resource = parent_resource

        # if values have been passed, so use them as objects attributes.
        # attributes are prefixed by an underscore '_'
        if _id is not None:
            self.__id = _id
        if alias is not None:
            self._alias = alias
        if dataType is not None:
            self._dataType = dataType
        if description is not None:
            self._description = description
        if isAutoGenerated is not None:
            self._isAutoGenerated = isAutoGenerated
        if isNullable is not None:
            self._isNullable = isNullable
        if isReadOnly is not None:
            self._isReadOnly = isReadOnly
        if hasElevation is not None:
            self._hasElevation = hasElevation
        if hasMeasure is not None:
            self._hasMeasure = hasMeasure
        if language is not None:
            self._language = language
        if length is not None:
            self._length = length
        if name is not None:
            self._name = name
        if precision is not None:
            self._precision = precision
        if scale is not None:
            self._scale = scale
        if spatialContext is not None:
            self._spatialContext = spatialContext
        if propertyType is not None:
            self._propertyType = propertyType
        # specific to this SDK
        if parent_resource is not None:
            self._parent_resource = parent_resource

    # -- PROPERTIES --------------------------------------------------------------------
    # UUID
    @property
    def _id(self) -> str:
        """Gets the id of this FeatureAttribute.

        :return: The id of this FeatureAttribute.
        :rtype: str
        """
        return self.__id

    # alias
    @property
    def alias(self) -> str:
        """Gets the alias of this FeatureAttribute.

        :return: The alias of this FeatureAttribute.
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias: str):
        """Sets the alias of this FeatureAttribute.

        :param str alias: The alias of this FeatureAttribute.
        """

        self._alias = alias

    # dataType
    @property
    def dataType(self) -> str:
        """Gets the dataType of this FeatureAttribute.

        :return: The dataType of this FeatureAttribute.
        :rtype: str
        """
        return self._dataType

    @dataType.setter
    def dataType(self, dataType: str):
        """Sets the dataType of this FeatureAttribute.

        :param str dataType: The dataType of this FeatureAttribute.
        """

        self._dataType = dataType

    # description
    @property
    def description(self) -> str:
        """Gets the description of this FeatureAttribute.

        :return: The description of this FeatureAttribute.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this FeatureAttribute.

        :param str description: The description of this FeatureAttribute. Accept markdown syntax.
        """

        self._description = description

    # language
    @property
    def language(self) -> str:
        """Gets the language of this FeatureAttribute.

        :return: The language of this FeatureAttribute.
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language: str):
        """Sets the language of this FeatureAttribute.

        :param str language: The language of this FeatureAttribute.
        """

        self._language = language

    # isAutoGenerated
    @property
    def isAutoGenerated(self) -> bool:
        """Gets the isAutoGenerated of this FeatureAttribute.

        :return: The isAutoGenerated of this FeatureAttribute.
        :rtype: bool
        """
        return self._isAutoGenerated

    @isAutoGenerated.setter
    def isAutoGenerated(self, isAutoGenerated: bool):
        """Sets the isAutoGenerated of this FeatureAttribute.

        :param bool isAutoGenerated: The isAutoGenerated of this FeatureAttribute.
        """

        self._isAutoGenerated = isAutoGenerated

    # isNullable
    @property
    def isNullable(self) -> bool:
        """Gets the isNullable of this FeatureAttribute.

        :return: The isNullable of this FeatureAttribute.
        :rtype: bool
        """
        return self._isNullable

    @isNullable.setter
    def isNullable(self, isNullable: bool):
        """Sets the isNullable of this FeatureAttribute.

        :param bool isNullable: The isNullable of this FeatureAttribute.
        """

        self._isNullable = isNullable

    # isReadOnly
    @property
    def isReadOnly(self) -> bool:
        """Gets the isReadOnly of this FeatureAttribute.

        :return: The isReadOnly of this FeatureAttribute.
        :rtype: bool
        """
        return self._isReadOnly

    @isReadOnly.setter
    def isReadOnly(self, isReadOnly: bool):
        """Sets the isReadOnly of this FeatureAttribute.

        :param bool isReadOnly: The isReadOnly of this FeatureAttribute.
        """

        self._isReadOnly = isReadOnly

    # hasElevation
    @property
    def hasElevation(self) -> bool:
        """Gets the hasElevation of this FeatureAttribute.

        :return: The hasElevation of this FeatureAttribute.
        :rtype: bool
        """
        return self._hasElevation

    @hasElevation.setter
    def hasElevation(self, hasElevation: bool):
        """Sets the hasElevation of this FeatureAttribute.

        :param bool hasElevation: The hasElevation of this FeatureAttribute.
        """

        self._hasElevation = hasElevation

    # hasMeasure
    @property
    def hasMeasure(self) -> bool:
        """Gets the hasMeasure of this FeatureAttribute.

        :return: The hasMeasure of this FeatureAttribute.
        :rtype: bool
        """
        return self._hasMeasure

    @hasMeasure.setter
    def hasMeasure(self, hasMeasure: bool):
        """Sets the hasMeasure of this FeatureAttribute.

        :param bool hasMeasure: The hasMeasure of this FeatureAttribute.
        """

        self._hasMeasure = hasMeasure

    # length
    @property
    def length(self) -> int:
        """Gets the length of this FeatureAttribute.

        :return: The length of this FeatureAttribute.
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length: int):
        """Sets the length of this FeatureAttribute.

        :param int length: The length of this FeatureAttribute.
        """

        self._length = length

    # name
    @property
    def name(self) -> str:
        """Gets the name of this FeatureAttribute.

        :return: The name of this FeatureAttribute.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this FeatureAttribute.

        :param str name: The name of this FeatureAttribute.
        """

        self._name = name

    # precision
    @property
    def precision(self) -> int:
        """Gets the precision of this FeatureAttribute.

        :return: The precision of this FeatureAttribute.
        :rtype: int
        """
        return self._precision

    @precision.setter
    def precision(self, precision: int):
        """Sets the precision of this FeatureAttribute.

        :param int precision: The precision of this FeatureAttribute.
        """

        self._precision = precision

    # propertyType
    @property
    def propertyType(self) -> str:
        """Gets the propertyType of this FeatureAttribute.

        :return: The propertyType of this FeatureAttribute.
        :rtype: str
        """
        return self._propertyType

    @propertyType.setter
    def propertyType(self, propertyType: str):
        """Sets the propertyType of this FeatureAttribute.

        :param str propertyType: The propertyType of this FeatureAttribute.
        """

        self._propertyType = propertyType

    # scale
    @property
    def scale(self) -> int:
        """Gets the scale of this FeatureAttribute.

        :return: The scale of this FeatureAttribute.
        :rtype: int
        """
        return self._scale

    @scale.setter
    def scale(self, scale: int):
        """Sets the scale of this FeatureAttribute.

        :param int scale: The scale of this FeatureAttribute.
        """

        self._scale = scale

    # spatialContext
    @property
    def spatialContext(self) -> str:
        """Gets the spatialContext of this FeatureAttribute.

        :return: The spatialContext of this FeatureAttribute.
        :rtype: str
        """
        return self._spatialContext

    @spatialContext.setter
    def spatialContext(self, spatialContext: str):
        """Sets the spatialContext of this FeatureAttribute.

        :param str spatialContext: The spatialContext of this FeatureAttribute.
        """

        self._spatialContext = spatialContext

    # -- METHODS -----------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Returns the model properties as a dict."""
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
        if issubclass(FeatureAttribute, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_dict_creation(self) -> dict:
        """Returns the model properties as a dict structured for creation purpose (POST)"""
        result = {}

        for attr, _ in self.attr_crea.items():
            # get attribute value
            value = getattr(self, attr)
            # switch attribute name for creation purpose
            if attr in self.ATTR_MAP:
                attr = self.ATTR_MAP.get(attr)
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
        if issubclass(FeatureAttribute, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other) -> bool:
        """Returns true if both objects are equal."""
        if not isinstance(other, FeatureAttribute):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Returns true if both objects are not equal."""
        return not self == other


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    """standalone execution."""
    fixture = FeatureAttribute()
