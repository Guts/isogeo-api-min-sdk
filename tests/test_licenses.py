# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_licenses
    # for licific
    python -m unittest tests.test_licenses.TestLicenses.test_licenses_create_basic
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# Standard library
from os import environ
import logging
from random import sample
from socket import gethostname
from sys import exit, _getframe
from time import gmtime, sleep, strftime
import unittest
import urllib3

# 3rd party
from dotenv import load_dotenv


# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, License, Metadata


# #############################################################################
# ######## Globals #################
# ##################################

load_dotenv("dev.env", override=True)

# host machine name - used as discriminator
hostname = gethostname()

# API access
app_script_id = environ.get("ISOGEO_API_USER_CLIENT_ID")
app_script_secret = environ.get("ISOGEO_API_USER_CLIENT_SECRET")
platform = environ.get("ISOGEO_PLATFORM", "qa")
user_email = environ.get("ISOGEO_USER_NAME")
user_password = environ.get("ISOGEO_USER_PASSWORD")
METADATA_TEST_FIXTURE_UUID = environ.get("ISOGEO_FIXTURES_METADATA_COMPLETE")
WORKGROUP_TEST_FIXTURE_UUID = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_UNIT_PythonSDK - Licenses - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestLicenses(unittest.TestCase):
    """Test License model of Isogeo API."""

    # -- Standard methods --------------------------------------------------------
    @classmethod
    def setUpClass(cls):
        """Executed when module is loaded before any test."""
        # checks
        if not app_script_id or not app_script_secret:
            logging.critical("No API credentials set as env variables.")
            exit()
        else:
            pass
        logging.debug("Isogeo PySDK version: {0}".format(pysdk_version))

        # class vars and attributes
        cls.li_fixtures_to_delete = []

        # ignore warnings related to the QA self-signed cert
        if environ.get("ISOGEO_PLATFORM").lower() == "qa":
            urllib3.disable_warnings()

        # API connection
        cls.isogeo = IsogeoSession(
            client_id=environ.get("ISOGEO_API_USER_CLIENT_ID"),
            client_secret=environ.get("ISOGEO_API_USER_CLIENT_SECRET"),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            platform=environ.get("ISOGEO_PLATFORM", "qa"),
        )
        # getting a token
        cls.isogeo.connect(username=user_email, password=user_password)

        # fixture metadata
        md = Metadata(title=get_test_marker(), type="vectorDataset")
        cls.fixture_metadata = cls.isogeo.metadata.create(
            WORKGROUP_TEST_FIXTURE_UUID, metadata=md, check_exists=0
        )

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        sleep(0.5)
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created metadata
        cls.isogeo.metadata.delete(cls.fixture_metadata._id)

        # clean created licenses
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.license.delete(
                    workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, license_id=i
                )
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------

    # -- POST --
    def test_licenses_create_basic(self):
        """POST :groups/{workgroup_uuid}/licenses/}"""
        # var
        license_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        license_new = License(name=license_name)

        # create it online
        license_new = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(license_new.name, license_name)
        self.assertTrue(self.isogeo.license.exists(license_new._id))

        # add created license to deletion
        self.li_fixtures_to_delete.append(license_new._id)

    def test_licenses_create_complete(self):
        """POST :groups/{workgroup_uuid}/licenses/}"""
        # populate model object locally
        license_new = License(
            name="{} - {}".format(get_test_marker(), self.discriminator),
            content="{} - **CONTENT** - {}".format(
                get_test_marker(), self.discriminator
            ),
            link="https://fr.wikipedia.org/wiki/Licence_Creative_Commons",
        )
        # create it online
        license_new = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_new,
            check_exists=0,
        )

        # checks
        self.assertEqual(
            license_new.name, "{} - {}".format(get_test_marker(), self.discriminator)
        )
        self.assertTrue(self.isogeo.license.exists(license_new._id))

        # add created license to deletion
        self.li_fixtures_to_delete.append(license_new._id)

    def test_licenses_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/licenses/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        license_local = License(name=name_to_be_unique)

        # create it online
        license_new_1 = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_local,
            check_exists=0,
        )

        # try to create a license with the same name
        license_new_2 = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_local,
            check_exists=1,
        )

        # check if object has not been created
        self.assertEqual(license_new_2, False)

        # add created license to deletion
        self.li_fixtures_to_delete.append(license_new_1._id)

    def test_licenses_association(self):
        """POST :resources/{metadata_uuid}/conditions/"""
        # create local object
        license_new = License(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )

        # create it online
        license_new = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_new,
            check_exists=0,
        )

        # associate it
        self.isogeo.license.associate_metadata(
            metadata=self.fixture_metadata,
            license=license_new,
            description="Testing license association",
        )

        # refresh fixture metadata
        self.fixture_metadata = self.isogeo.metadata.get(
            metadata_id=self.fixture_metadata._id, include=["conditions"]
        )

        # try to associate the same license = error
        asso_fail = self.isogeo.license.associate_metadata(
            metadata=self.fixture_metadata,
            license=license_new,
            description="Testing license association",
        )
        self.assertIsInstance(asso_fail, tuple)
        self.assertFalse(asso_fail[0])

        # try to associate the same license with force option = ok
        self.isogeo.license.associate_metadata(
            metadata=self.fixture_metadata,
            license=license_new,
            description="Testing license association - forced",
            force=1,
        )

        # -- dissociate
        # refresh fixture metadata
        self.fixture_metadata = self.isogeo.metadata.get(
            metadata_id=self.fixture_metadata._id, include=["conditions"]
        )
        for condition in self.fixture_metadata.conditions:
            self.isogeo.license.dissociate_metadata(
                metadata=self.fixture_metadata, condition_id=condition.get("_id")
            )

        # add created license to deletion
        self.li_fixtures_to_delete.append(license_new._id)

    # -- GET --
    def test_licenses_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/licenses}"""
        # retrieve workgroup licenses
        wg_licenses = self.isogeo.license.listing(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=1
        )
        self.assertIsInstance(wg_licenses, list)
        # parse and test object loader
        for i in wg_licenses:
            lic = License(**i)
            # tests attributes structure
            self.assertTrue(hasattr(lic, "_abilities"))
            self.assertTrue(hasattr(lic, "_id"))
            self.assertTrue(hasattr(lic, "_tag"))
            self.assertTrue(hasattr(lic, "link"))
            self.assertTrue(hasattr(lic, "name"))
            self.assertTrue(hasattr(lic, "content"))
            self.assertTrue(hasattr(lic, "owner"))
            # tests attributes value
            self.assertEqual(lic.link, i.get("link"))
            self.assertEqual(lic.name, i.get("name"))
            self.assertEqual(lic.content, i.get("content"))

    def test_license_detailed(self):
        """GET :licenses/{license_uuid}"""
        # retrieve workgroup licenses
        if self.isogeo._wg_licenses_names:
            wg_licenses = self.isogeo._wg_licenses_names
        else:
            wg_licenses = self.isogeo.license.listing(
                workgroup_id=WORKGROUP_TEST_FIXTURE_UUID, caching=0
            )

        # pick two licenses: one locked by Isogeo, one workgroup specific
        license_id_isogeo = sample(
            list(filter(lambda d: "isogeo" in d.get("_tag"), wg_licenses)), 1
        )[0]
        license_id_specific = sample(
            list(filter(lambda d: "isogeo" not in d.get("_tag"), wg_licenses)), 1
        )[0]

        # check both exist
        self.assertTrue(self.isogeo.license.exists(license_id_isogeo.get("_id")))
        self.assertTrue(self.isogeo.license.exists(license_id_specific.get("_id")))

        # get and check both
        license_isogeo = self.isogeo.license.license(license_id_isogeo.get("_id"))
        license_specific = self.isogeo.license.license(license_id_specific.get("_id"))
        self.assertIsInstance(license_isogeo, License)
        self.assertIsInstance(license_specific, License)

    # -- PUT/PATCH --
    def test_licenses_update(self):
        """PUT :groups/{workgroup_uuid}/licenses/{license_uuid}"""
        # create a new license
        license_fixture = License(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )
        license_fixture = self.isogeo.license.create(
            workgroup_id=WORKGROUP_TEST_FIXTURE_UUID,
            license=license_fixture,
            check_exists=0,
        )

        # modify local object
        license_fixture.name = "{} - {}".format(get_test_marker(), self.discriminator)
        license_fixture.content = "{} content - {}".format(
            get_test_marker(), self.discriminator
        )
        license_fixture.link = "https://github.com/isogeo/isogeo-api-py-minsdk"

        # update the online license
        license_fixture = self.isogeo.license.update(license_fixture)

        # check if the change is effective
        license_fixture_updated = self.isogeo.license.license(license_fixture._id)
        self.assertEqual(
            license_fixture_updated.name,
            "{} - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertEqual(
            license_fixture_updated.content,
            "{} content - {}".format(get_test_marker(), self.discriminator),
        )
        self.assertEqual(
            license_fixture_updated.link,
            "https://github.com/isogeo/isogeo-api-py-minsdk",
        )

        # add created license to deletion
        self.li_fixtures_to_delete.append(license_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if get_test_marker() == "__main__":
    unittest.main()
