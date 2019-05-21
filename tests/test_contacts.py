# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_contacts
    # for specific
    python -m unittest tests.test_contacts.TestContacts.test_contacts_create_basic
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
from time import gmtime, strftime
import unittest

# 3rd party
from dotenv import load_dotenv
from oauthlib.oauth2 import LegacyApplicationClient

# module target
from isogeo_pysdk import IsogeoSession, __version__ as pysdk_version, Contact


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
workgroup_test = environ.get("ISOGEO_WORKGROUP_TEST_UUID")

# #############################################################################
# ########## Helpers ###############
# ##################################


def get_test_marker():
    """Returns the function name"""
    return "TEST_UNIT_PythonSDK - {}".format(_getframe(1).f_code.co_name)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestContacts(unittest.TestCase):
    """Test Contact model of Isogeo API."""

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

        # API connection
        cls.isogeo = IsogeoSession(
            client=LegacyApplicationClient(
                client_id=environ.get("ISOGEO_API_USER_CLIENT_ID")
            ),
            auto_refresh_url="{}/oauth/token".format(environ.get("ISOGEO_ID_URL")),
            client_secret=app_script_secret,
            platform=platform,
        )
        # getting a token
        cls.isogeo.connect(username=user_email, password=user_password)

    def setUp(self):
        """Executed before each test."""
        # tests stuff
        self.discriminator = "{}_{}".format(
            hostname, strftime("%Y-%m-%d_%H%M%S", gmtime())
        )

    def tearDown(self):
        """Executed after each test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Executed after the last test."""
        # clean created contacts
        if len(cls.li_fixtures_to_delete):
            for i in cls.li_fixtures_to_delete:
                cls.isogeo.contact.contact_delete(
                    workgroup_id=workgroup_test, contact_id=i
                )
        # close sessions
        cls.isogeo.close()

    # -- TESTS ---------------------------------------------------------
    # -- POST --
    def test_contacts_create_basic(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # var
        contact_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create local object
        contact_new = Contact(name=contact_name)

        # create it online
        contact_new = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_new, check_exists=0
        )

        # checks
        self.assertEqual(contact_new.name, contact_name)
        self.assertTrue(self.isogeo.contact.contact_exists(contact_new._id))

        # add created specification to deletion
        self.li_fixtures_to_delete.append(contact_new._id)

    def test_contacts_create_complete(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # var
        contact_name = "{} - {}".format(get_test_marker(), self.discriminator)

        # create a complete local object
        contact_new = Contact(
            addressLine1="26 rue du faubourg Saint-Antoine",
            addressLine2="4è étage",
            addressLine3="Porte rouge",
            name=contact_name,
            city="Paris",
            email="test@isogeo.fr",
            fax="+33987654321",
            organization="Isogeo",
            phone="+33789456123",
            countryCode="FR",
            zipCode="75012",
        )
        contact_new = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_new
        )

        # checks
        self.assertEqual(contact_new.name, contact_name)
        self.assertEqual(contact_new.type, "custom")
        self.assertTrue(self.isogeo.contact.contact_exists(contact_new._id))

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new._id)

    def test_contacts_create_checking_name(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # vars
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        contact_local = Contact(name=name_to_be_unique)

        # create it online
        contact_new_1 = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_local, check_exists=0
        )

        # try to create a contact with the same name
        contact_new_2 = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_local, check_exists=1
        )

        # check if object has not been created
        self.assertEqual(contact_new_2, False)

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new_1._id)

    def test_contacts_create_checking_email(self):
        """POST :groups/{workgroup_uuid}/contacts/}"""
        # vars
        email_to_be_unique = "test@isogeo.fr"
        name_to_be_unique = "TEST_UNIT_AUTO UNIQUE"

        # create local object
        contact_local = Contact(email=email_to_be_unique, name=name_to_be_unique)

        # create it online
        contact_new_1 = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_local, check_exists=0
        )

        # try to create a contact with the same email
        contact_new_2 = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_local, check_exists=2
        )

        # check if object has not been created
        self.assertEqual(contact_new_2, False)

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_new_1._id)

    # -- GET --
    def test_contacts_get_workgroup(self):
        """GET :groups/{workgroup_uuid}/contacts}"""
        # retrieve workgroup contacts
        wg_contacts = self.isogeo.contact.contacts(
            workgroup_id=workgroup_test, caching=1
        )
        self.assertIsInstance(wg_contacts, list)
        # parse and test object loader
        for i in wg_contacts:
            contact = Contact(**i)
            # tests attributes structure
            self.assertTrue(hasattr(contact, "_abilities"))
            self.assertTrue(hasattr(contact, "_id"))
            self.assertTrue(hasattr(contact, "_tag"))
            self.assertTrue(hasattr(contact, "_addressLine1"))
            self.assertTrue(hasattr(contact, "_addressLine2"))
            self.assertTrue(hasattr(contact, "_addressLine3"))
            self.assertTrue(hasattr(contact, "_city"))
            self.assertTrue(hasattr(contact, "_count"))
            self.assertTrue(hasattr(contact, "name"))
            self.assertTrue(hasattr(contact, "owner"))
            self.assertTrue(hasattr(contact, "zipCode"))
            # tests attributes value
            self.assertEqual(contact.addressLine1, i.get("addressLine1"))
            self.assertEqual(contact.name, i.get("name"))
            self.assertEqual(contact.zipCode, i.get("zipCode"))

    def test_contact_detailed(self):
        """GET :contacts/{contact_uuid}"""
        # retrieve workgroup contacts
        if self.isogeo._wg_contacts_names:
            wg_contacts = self.isogeo._wg_contacts_names
        else:
            wg_contacts = self.isogeo.contact.contacts(
                workgroup_id=workgroup_test, caching=0
            )

        # pick three contacts: one locked by Isogeo, one workgroup specific, on user (deprecated)
        contact_id_isogeo = sample(
            list(filter(lambda d: "group" in d.get("_tag"), wg_contacts)), 1
        )[0]
        contact_id_specific = sample(
            list(filter(lambda d: workgroup_test in d.get("_tag"), wg_contacts)), 1
        )[0]
        # contact_id_user = sample(
        #     list(filter(lambda d: "user" in d.get("_tag"), wg_contacts)), 1
        # )[0]

        # check both exist
        self.assertTrue(
            self.isogeo.contact.contact_exists(contact_id_isogeo.get("_id"))
        )
        self.assertTrue(
            self.isogeo.contact.contact_exists(contact_id_specific.get("_id"))
        )
        # self.assertTrue(
        #     self.isogeo.contact.contact_exists(
        #         contact_id_user.get("_id")
        #     )
        # )

        # get and check
        contact_isogeo = self.isogeo.contact.contact(contact_id_isogeo.get("_id"))
        contact_specific = self.isogeo.contact.contact(contact_id_specific.get("_id"))
        # contact_user = self.isogeo.contact.contact(
        #     contact_id_user.get("_id")
        # )

        self.assertIsInstance(contact_isogeo, Contact)
        self.assertIsInstance(contact_specific, Contact)
        # self.assertIsInstance(contact_user, Contact)

    # -- PUT/PATCH --
    def test_contacts_update(self):
        """PUT :groups/{workgroup_uuid}/contacts/{contact_uuid}}"""
        # create a new contact
        contact_fixture = Contact(
            name="{} - {}".format(get_test_marker(), self.discriminator)
        )
        contact_fixture = self.isogeo.contact.contact_create(
            workgroup_id=workgroup_test, contact=contact_fixture, check_exists=0
        )

        # modify local object
        contact_fixture.name = "{} - UPDATED - {}".format(
            get_test_marker(), self.discriminator
        )

        # update the online contact
        contact_fixture = self.isogeo.contact.contact_update(contact_fixture)

        # check if the change is effective
        contact_fixture_updated = self.isogeo.contact.contact(contact_fixture._id)
        self.assertEqual(
            contact_fixture_updated.name,
            "{} - UPDATED - {}".format(get_test_marker(), self.discriminator),
        )

        # add created contact to deletion
        self.li_fixtures_to_delete.append(contact_fixture_updated._id)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
