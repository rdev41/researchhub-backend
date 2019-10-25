from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from utils.test_helpers import IntegrationTestHelper, TestHelper


class PaperTests(TestCase, TestHelper):

    def test_string_representation(self):
        paper = self.create_paper_without_authors()
        text = '%s: []' % self.test_data.paper_title
        self.assertEqual(str(paper), text)


class PaperIntegrationTests(
    TestCase,
    TestHelper,
    IntegrationTestHelper
):
    base_url = '/api/paper/'

    def test_get_base_route(self):
        response = self.get_get_response(self.base_url)
        self.assertEqual(response.status_code, 200)

    def test_upload_paper(self):
        response = self.submit_paper_form()
        text = 'The Simple Paper'
        self.assertContains(response, text, status_code=201)

    def submit_paper_form(self):
        client = self.get_default_authenticated_client()
        url = self.base_url
        form_data = self.build_paper_form()
        response = client.post(url, form_data)
        return response

    def build_paper_form(self):
        print('build_paper_form')
        file = SimpleUploadedFile('../config/paper.pdf', b'file_content')
        hub = self.create_hub('Film')
        university = self.create_university(name='Charleston')
        author = self.create_author_without_user(
            university,
            first_name='Donald',
            last_name='Duck'
        )

        form = {
            'title': 'The Simple Paper',
            'paper_publish_date': self.paper_publish_date,
            'file': file,
            'hubs': [hub.id],
            'authors': [author.id],
        }
        return form