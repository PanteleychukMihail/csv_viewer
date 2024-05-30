from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from csv_app.csv_processor import CSVProcessor, MongoDBManager


class TestUploadCSVView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csv_app/csv_loader.html')


class CSVProcessorTests(TestCase):
    def setUp(self):
        self.db_manager = MongoDBManager()

    def test_is_valid_csv_with_valid_file(self):
        valid_csv_content = b"header1,header2,header3\nvalue1,value2,value3\n"
        valid_csv_file = SimpleUploadedFile("test.csv", valid_csv_content)
        processor = CSVProcessor(self.db_manager)
        self.assertTrue(processor.is_valid_csv(valid_csv_file))

    def test_is_valid_csv_with_invalid_file(self):
        invalid_csv_content = b"212121212121212"
        invalid_csv_file = SimpleUploadedFile("test.csv", invalid_csv_content)
        print(invalid_csv_file)
        processor = CSVProcessor(self.db_manager)
        self.assertFalse(processor.is_valid_csv(invalid_csv_file))

    def test_get_collection_name(self):
        headers = ["header1", "header2", "header3"]
        file_name = "test.csv"
        processor = CSVProcessor(self.db_manager)
        collection_name = processor.get_collection_name(file_name, headers)
        expected_collection_name = "test.csv_bd92b767f3c6e8944403f7cf91b3129ce8044c3ee3dfb03504cc29ba6166fcb5"
        self.assertEqual(collection_name, expected_collection_name)

    def test_post_with_valid_csv_file(self):
        valid_csv_content = b"header1,header2,header3\nvalue1,value2,value3\n"
        valid_csv_file = SimpleUploadedFile("test.csv", valid_csv_content)
        response = self.client.post(reverse('upload_csv'), {'csv_file': valid_csv_file})
        self.assertEqual(response.status_code, 302)

    def test_post_with_invalid_csv_file(self):
        invalid_csv_content = b"not a csv file"
        invalid_csv_file = SimpleUploadedFile("invalid.csv", invalid_csv_content)
        response = self.client.post(reverse('upload_csv'), {'csv_file': invalid_csv_file})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('upload_csv'))
