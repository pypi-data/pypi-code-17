from rng_to_form.rng import RNG
from unittest import TestCase, main


class RngTest(TestCase):

    def setUp(self):
        self.file = "./tests/data/test.rng"

    def test_create_rng_obj(self):
        rng = RNG(file=self.file, target="ArchiveTransfer")
        self.assertIsNotNone(rng)

    def test_form_root(self):
        rng = RNG(file=self.file, target="ArchiveTransfer")
        groot = rng.get_form_root(root_name="ArchiveTransfer")
        self.assertEqual(groot, "ArchiveTransfer_N65537")

    def test_find_definitions(self):
        rng = RNG(file=self.file, target="ArchiveTransfer")
        ordered = rng.find_definitions()
        self.assertEqual(ordered, {'ArchivalAgency_N65594': ['Identification_N65597', 'Name_N65632'],
            'Archive_N65696': ['ArchivalAgreement_N65700', 'ArchivalProfile_N65733', 'DescriptionLanguage_N65766',
            'Name_N65780', 'TransferringAgencyArchiveIdentifier_N65792', 'ContentDescription_N65825', 'AccessRestrictionRule_N66085',
            'AppraisalRule_N66117', 'ArchiveObject_N66157', 'ArchiveObject_N66326', 'ArchiveObject_N66493'],
            'Integrity_N66265': ['value', 'algorithme'], 'Comment_N65541': ['value'],
            'ArchiveTransfer_N65537': ['Comment_N65541', 'Date', 'TransferIdentifier_N65562', 'ArchivalAgency_N65594',
            'TransferringAgency_N65646', 'Archive_N65696'], 'ContentDescription_N66509': ['Description_N66513', 'DescriptionLevel_N66527',
            'Language_N66540'], 'ContentDescription_N65825': ['Description_N65830', 'DescriptionLevel_N65844', 'FilePlanPosition_N65857',
            'Language_N65891', 'LatestDate', 'OldestDate', 'CustodialHistory_N65922', 'Keyword_N65949', 'Keyword_N65981', 'OriginatingAgency_N66013'],
            'Document_N66228': ['Attachment_N66233', 'Integrity_N66265', 'Size_N66278', 'Type_N66291'],
            'Description_N66513': ['value'], 'Name_N65780': ['value'], 'KeywordContent_N65954': ['value'], 'Name_N66498': ['value'],
            'Attachment_N66566': ['value', 'format', 'filename'], 'Integrity_N66598': ['value', 'algorithme'],
            'ArchiveObject_N66493': ['Name_N66498', 'ContentDescription_N66509', 'Document_N66561'],
            'DescriptionLevel_N66527': ['value', 'listVersionID'], 'Name_N66331': ['value'],
            'Identification_N65597': ['value', 'schemeName', 'schemeAgencyName'], 'Description_N66018': ['value'],
            'Language_N66540': ['value', 'listVersionID'], 'Type_N66291': ['value', 'listVersionID'],
            'ContentDescription_N66359': ['DescriptionLevel_N66363', 'Language_N66376'], 'Size_N66278': ['value', 'unitCode'],
            'ArchivalAgreement_N65700': ['value'], 'TransferringAgencyArchiveIdentifier_N65792': ['value'],
            'Code_N66122': ['value', 'listVersionID'], 'Size_N66611': ['value', 'unitCode'], 'KeywordContent_N65986': ['value'],
            'ArchiveObject_N66342': ['Name_N66347', 'ContentDescription_N66359', 'Document_N66397'],
            'OriginatingAgency_N66013': ['Description_N66018', 'Identification_N66031', 'Name_N66066'],
            'ArchiveObject_N66157': ['Name_N66162', 'ArchiveObject_N66173'], 'Keyword_N65949': ['KeywordContent_N65954'],
            'DescriptionLevel_N66194': ['value', 'listVersionID'], 'Attachment_N66233': ['value', 'format', 'filename'],
            'Name_N66162': ['value'], 'Language_N66207': ['value', 'listVersionID'], 'Language_N65891': ['value', 'listVersionID'],
            'TransferringAgency_N65646': ['Identification_N65649', 'Name_N65684'], 'Type_N66458': ['value', 'listVersionID'],
            'Document_N66397': ['Attachment_N66402', 'Integrity_N66434', 'Size_N66445', 'Type_N66458'],
            'DescriptionLevel_N65844': ['value', 'listVersionID'], 'Name_N65684': ['value'],
            'Description_N65830': ['value'], 'ArchiveObject_N66326': ['Name_N66331', 'ArchiveObject_N66342'],
            'Attachment_N66402': ['value', 'format', 'filename'], 'CustodialHistory_N65922': ['CustodialHistoryItem_N65927'],
            'AppraisalRule_N66117': ['Code_N66122', 'Duration', 'StartDate'], 'Type_N66624': ['value', 'listVersionID'],
            'CustodialHistoryItem_N65927': ['value'], 'FilePlanPosition_N65857': ['value'], 'ArchiveObject_N66173': ['Name_N66178',
            'ContentDescription_N66190', 'Document_N66228'], 'Name_N66066': ['value'], 'Document_N66561': ['Attachment_N66566', 'Integrity_N66598',
            'Size_N66611', 'Type_N66624'], 'Language_N66376': ['value', 'listVersionID'], 'Integrity_N66434': ['value', 'algorithme'],
            'AccessRestrictionRule_N66085': ['Code_N66088', 'StartDate'], 'Identification_N66031': ['value', 'schemeName', 'schemeAgencyName'],
            'DescriptionLanguage_N65766': ['value', 'listVersionID'], 'Size_N66445': ['value', 'unitCode'],
            'ContentDescription_N66190': ['DescriptionLevel_N66194', 'Language_N66207'], 'Identification_N65649': ['value', 'schemeName', 'schemeAgencyName'],
            'Name_N66178': ['value'], 'Name_N65632': ['value'], 'Name_N66347': ['value'], 'ArchivalProfile_N65733': ['value'],
            'TransferIdentifier_N65562': ['value'], 'Code_N66088': ['value', 'listVersionID'], 'ArchiveTransfer': ['ArchiveTransfer_N65537'],
            'DescriptionLevel_N66363': ['value', 'listVersionID'], 'Keyword_N65981': ['KeywordContent_N65986']})


if __name__ == '__main__':
    main()
