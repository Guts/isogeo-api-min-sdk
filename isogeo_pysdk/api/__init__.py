# coding: utf-8
#! python3  # noqa: E265

from .routes_application import ApiApplication  # noqa: F401
from .routes_account import ApiAccount  # noqa: F401
from .routes_catalog import ApiCatalog  # noqa: F401
from .routes_contact import ApiContact  # noqa: F401
from .routes_datasource import ApiDatasource  # noqa: F401
from .routes_keyword import ApiKeyword  # noqa: F401
from .routes_license import ApiLicense  # noqa: F401
from .routes_resource import ApiResource  # noqa: F401
from .routes_share import ApiShare  # noqa: F401
from .routes_service_layers import ApiServiceLayer  # noqa: F401
from .routes_service_operations import ApiServiceOperation  # noqa: F401
from .routes_specification import ApiSpecification  # noqa: F401
from .routes_thesaurus import ApiThesaurus  # noqa: F401
from .routes_workgroup import ApiWorkgroup  # noqa: F401

# shortcuts or confusion reducers
ApiMetadata = ApiResource