from flask_testing import TestCase
from simpleweb import app
import unittest
import json


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app


class TestingService(BaseTestCase):

    def test_1_get(self):
        print "\n Test: test_1_get"

        headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
        url = '/'

        response = self.client.get(url, headers=headers)

        self.assertEquals(json.loads(response.json), "Your API is running!")


if __name__ == '__main__':
    unittest.main()
