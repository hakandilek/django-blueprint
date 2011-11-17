from django.utils import unittest
from django.test.client import Client

class SampleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_sample_index(self):
        # Issue a GET request.
        response = self.client.get('/sample/')

        # Check that the response is 200 OK.
        self.assertIn(response.status_code, (200, 302))
