import unittest
from flask import Flask
from app import create_app, mongo


class TestWelcomeRoute(unittest.TestCase):
    '''Test the welcome route'''

    @classmethod
    def setUpClass(cls):
        '''Set up the test client'''
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        '''Close the app context'''
        mongo.cx.close()
        cls.app_context.pop()

    def test_welcome_route(self):
        """Test the welcome route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Welcome to the Weather Advisor API!"})

    def test_welcome_route_method_not_allowed(self):
        '''Test that POST method is not allowed on the welcome route'''
        response = self.client.post('/')

        self.assertEqual(response.status_code, 405)

    def test_welcome_route_content_type(self):
        '''Test that the content type of the response is JSON'''
        response = self.client.get('/')

        self.assertEqual(response.content_type, 'application/json')


if __name__ == '__main__':
    '''Run the tests'''
    unittest.main()
