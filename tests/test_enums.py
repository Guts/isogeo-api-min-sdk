# -*- coding: UTF-8 -*-
#! python3

"""
    Usage from the repo root folder:

    ```python
    # for whole test
    python -m unittest tests.test_enums
    # for specific
    python -m unittest tests.test_enums.TestEnums
    ```
"""

# #############################################################################
# ########## Libraries #############
# ##################################

# standard library
import unittest

# module target
from isogeo_pysdk.enums import (
    ApplicationTypes,
    ContactRoles,
    ContactTypes,
    EditionProfiles,
    EventKinds,
    KeywordCasing,
    LinkActions,
    LinkKinds,
    LinkTypes,
    MetadataTypes,
    MetadataSubresources,
    SessionStatus,
    ShareTypes,
    StatisticsTags,
)


# #############################################################################
# ########## Classes ###############
# ##################################


class TestEnums(unittest.TestCase):
    """Test Enum model of Isogeo API."""

    def setUp(self):
        """Executed before each test."""
        pass

    def tearDown(self):
        """Executed after each test."""
        pass

    # -- TESTS ---------------------------------------------------------

    def test_application_types(self):
        """Check metadata's types list"""
        self.assertEqual(len(ApplicationTypes), 2)
        self.assertTrue("group" in ApplicationTypes.__members__)
        self.assertFalse("User" in ApplicationTypes.__members__)
        for i in ApplicationTypes:
            self.assertIsInstance(i.value, int)

    def test_contact_roles(self):
        """Check contact's roles list"""
        self.assertEqual(len(ContactRoles), 11)
        self.assertTrue("author" in ContactRoles.__members__)
        self.assertFalse("Author" in ContactRoles.__members__)
        for i in ContactRoles:
            self.assertIsInstance(i.value, str)

    def test_contact_types(self):
        """Check contact's types list"""
        self.assertEqual(len(ContactTypes), 3)
        self.assertTrue("group" in ContactTypes.__members__)
        self.assertFalse("Custom" in ContactTypes.__members__)
        for i in ContactTypes:
            self.assertIsInstance(i.value, int)

    def test_edition_profiles(self):
        """Check edition profiles list"""
        self.assertEqual(len(EditionProfiles), 2)
        self.assertTrue("csw" in EditionProfiles.__members__)
        self.assertFalse("Manual" in EditionProfiles.__members__)
        for i in EditionProfiles:
            self.assertIsInstance(i.value, int)

    def test_event_kinds(self):
        """Check metadata's types list"""
        self.assertEqual(len(EventKinds), 3)
        self.assertTrue("creation" in EventKinds.__members__)
        self.assertFalse("Update" in EventKinds.__members__)
        for i in EventKinds:
            self.assertIsInstance(i.value, int)

    def test_keyword_casing(self):
        """Check keyword casing values list"""
        self.assertEqual(len(KeywordCasing), 4)
        self.assertTrue("capitalized" in KeywordCasing.__members__)
        self.assertFalse("Uppercase" in KeywordCasing.__members__)
        for i in KeywordCasing:
            self.assertIsInstance(i.value, int)

    def test_link_action(self):
        """Check link actions values list"""
        self.assertEqual(len(LinkActions), 3)
        self.assertTrue("download" in LinkActions.__members__)
        self.assertFalse("Other" in LinkActions.__members__)
        for i in LinkActions:
            self.assertIsInstance(i.value, int)

    def test_link_kind(self):
        """Check link kinds values list"""
        self.assertEqual(len(LinkKinds), 8)
        self.assertTrue("wms" in LinkKinds.__members__)
        self.assertFalse("EsriFeatureDataset" in LinkKinds.__members__)
        for i in LinkKinds:
            self.assertIsInstance(i.value, int)

    def test_link_type(self):
        """Check link types values list"""
        self.assertEqual(len(LinkTypes), 3)
        self.assertTrue("hosted" in LinkTypes.__members__)
        self.assertFalse("Link" in LinkTypes.__members__)
        for i in LinkTypes:
            self.assertIsInstance(i.value, int)

    def test_metadata_subresources(self):
        """Check metadata's subresources list"""
        self.assertEqual(len(MetadataSubresources), 14)
        self.assertTrue("tags" in MetadataSubresources.__members__)
        self.assertTrue(MetadataSubresources.has_value("feature-attributes"))
        self.assertFalse("Links" in MetadataSubresources.__members__)
        for i in MetadataSubresources:
            self.assertIsInstance(i.value, str)

    def test_metadata_types(self):
        """Check metadata's types list"""
        self.assertEqual(len(MetadataTypes), 4)
        self.assertTrue("rasterDataset" in MetadataTypes.__members__)
        self.assertFalse("Service" in MetadataTypes.__members__)
        for i in MetadataTypes:
            self.assertIsInstance(i.value, str)

    def test_session_status(self):
        """Check session statuses list"""
        self.assertEqual(len(SessionStatus), 4)
        self.assertTrue("started" in SessionStatus.__members__)
        self.assertFalse("Failed" in SessionStatus.__members__)
        for i in SessionStatus:
            self.assertIsInstance(i.value, int)

    def test_share_types(self):
        """Check share types list"""
        self.assertEqual(len(ShareTypes), 2)
        self.assertTrue("application" in ShareTypes.__members__)
        self.assertFalse("Group" in ShareTypes.__members__)
        for i in ShareTypes:
            self.assertIsInstance(i.value, int)

    def test_statistics_tags(self):
        """Check workgroup statistics tags names"""
        self.assertEqual(len(StatisticsTags), 6)
        self.assertTrue("catalog" in StatisticsTags.__members__)
        self.assertFalse("Catalog" in StatisticsTags.__members__)  # case sensitive
        self.assertTrue(StatisticsTags.has_value("coordinate-system"))
        for i in StatisticsTags:
            self.assertIsInstance(i.value, str)


# ##############################################################################
# ##### Stand alone program ########
# ##################################
if __name__ == "__main__":
    unittest.main()
