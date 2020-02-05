from django.test import TestCase

from allauth.socialaccount.providers.orcid.provider import OrcidProvider

from oauth.tests.helpers import create_social_account
from user.tests.helpers import create_random_default_user


class UserModelsTests(TestCase):

    def test_user_orcid_id(self):
        user = create_random_default_user('orcid')
        orcid_id = '0000-0002-0729-2718'
        create_social_account(OrcidProvider.id, user, uid=orcid_id)
        self.assertEqual(user.author_profile.orcid_id, orcid_id)
