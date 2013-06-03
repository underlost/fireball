from django.test import TestCase
from django.test.client import Client


# pylint: disable-msg=R0904
# pylint: disable-msg=E1103


class RecentblobsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = '/api/blob/?format=json'

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
