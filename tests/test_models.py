#!/usr/bin/env python
import unittest
from unittest.mock import patch
from app.models import get_coordinates
from app import create_app


class TestModels(unittest.TestCase):
    ''' Test the models module '''
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "lat": 51.5074,
            "lng": 0.1278
        }

        response = get_coordinates("London")
        self.assertEqual(response, {"lat": 51.5074, "lng": 0.1278})
        mock_get.assert_called_once()

    def tearDown(self):
        self.app_context.pop()


if __name__ == '__main__':
    ''' Run the tests '''
    unittest.main()
