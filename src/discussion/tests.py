import random

from django.test import TestCase
from django.contrib.sites.models import Site

from .models import Thread, Comment, Reply
from utils.test_helpers import IntegrationTestHelper, TestHelper


class BaseTestCase(TestCase, TestHelper):
    site = Site.objects.get_current()

    thread_title = 'Thread Title'
    thread_text = 'This is a thread.'
    comment_text = 'This is a comment.'
    reply_text = 'This is a reply.'

    def create_default_reply(self):
        comment = self.create_default_comment()
        user = self.create_random_default_user('reply')
        text = self.reply_text
        reply = self.create_reply(comment, user, text)
        return reply

    def create_reply(self, parent, user, text):
        reply = Reply.objects.create(
            parent=parent,
            created_by=user,
            text=text
        )
        return reply

    def create_default_comment(self):
        thread = self.create_default_thread()
        user = self.create_random_default_user('comment')
        text = self.comment_text
        comment = self.create_comment(thread, user, text)
        return comment

    def create_comment(self, thread, user, text):
        comment = Comment.objects.create(
            parent=thread,
            created_by=user,
            text=text
        )
        return comment

    def create_default_thread(self):
        paper = self.create_paper_without_authors()
        user = self.create_random_default_user('thread')
        title = self.thread_title
        text = self.thread_text
        thread = self.create_thread(paper, user, title, text)
        return thread

    def create_thread(self, paper, user, title, text):
        thread = Thread.objects.create(
            paper=paper,
            created_by=user,
            title=title,
            text=text
        )
        return thread


class ThreadTests(BaseTestCase):

    def test_string_representation(self):
        thread = self.create_default_thread()
        self.assertEqual(
            str(thread),
            'threadtestuser@gmail.com: Thread Title'
        )


class ReplyTests(BaseTestCase):

    def test_reply_to_reply(self):
        user = self.create_user()
        reply = self.create_default_reply()
        text = self.reply_text + ' 2'
        reply2 = self.create_reply(
            reply,
            user,
            text
        )
        self.assertEqual(reply2.parent, reply)


class BaseIntegrationTestCase(BaseTestCase, IntegrationTestHelper):
    base_url = '/api/paper/'

    def post_default_thread(self):
        paper = self.create_paper_without_authors()
        response = self.submit_thread_form(paper.id)
        return (response, paper.id)

    def submit_thread_form(self, paper_id):
        client = self.get_default_authenticated_client()
        url = self.base_url + f'{paper_id}/discussion/'
        form_data = self.build_default_thread_form(paper_id)
        response = client.post(url, form_data)
        return response

    def get_thread_submission_response(self, paper_id):
        user = self.create_random_authenticated_user('unique_value')
        url = self.base_url + f'{paper_id}/discussion/'
        form_data = self.build_default_thread_form(paper_id)
        response = self.get_authenticated_post_response(
            user,
            url,
            form_data,
            content_type='multipart/form-data'
        )
        return response

    def build_default_thread_form(self, paper_id):
        title = self.thread_title
        text = self.thread_text
        form = {
            'title': title,
            'text': text,
            'paper': paper_id
        }
        return form

    def parse_thread_title(self, thread_data):
        RESPONSE = 0
        thread = thread_data[RESPONSE]
        thread_json = self.bytes_to_json(thread.content)
        title = thread_json.get('title')
        return title

    def build_discussion_url(self, thread_data):
        PAPER_ID = 1
        paper_id = thread_data[PAPER_ID]
        url = self.base_url + f'{paper_id}/discussion/'
        return url


class DiscussionIntegrationTests(BaseIntegrationTestCase):

    def setUp(self):
        SEED = 'discussion'
        self.random_generator = random.Random(SEED)

    def test_discussion_view_shows_threads(self):
        thread = self.create_default_thread()
        paper_id = thread.paper.id
        url = self.base_url + f'{paper_id}/discussion/'
        response = self.get_get_response(url)
        text = thread.title
        self.assertContains(response, text, status_code=200)

    def test_create_thread(self):
        user = self.create_user_with_reputation(1)
        response = self.get_thread_submission_response(user)
        text = self.thread_title
        self.assertContains(response, text, status_code=201)

    def test_thread_is_created_by_current_user(self):
        user = self.create_user_with_reputation(1)
        response = self.get_thread_submission_response(user)
        response_user = self.get_user_from_response(response)
        text = response_user.id
        self.assertContains(response, text, status_code=201)

    def create_user_with_reputation(self, reputation):
        unique_value = self.random_generator.random()
        user = self.create_random_authenticated_user(unique_value)
        user.reputation = reputation
        user.save()
        return user

    def get_thread_submission_response(self, user):
        paper = self.create_paper_without_authors()
        paper_id = paper.id
        url = self.base_url + f'{paper_id}/discussion/'
        form_data = self.build_default_thread_form(paper_id)
        response = self.get_authenticated_post_response(
            user,
            url,
            form_data,
            content_type='multipart/form-data'
        )
        return response
