import unittest
from unittest.mock import patch, Mock
from app import create_app, mongo, cache


class TestRecommendRoute(unittest.TestCase):
    '''Test the recommend route'''

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

    def test_recommend_activity_missing_city(self):
        '''Test that the city parameter is required'''
        response = self.client.get('/recommend')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {"error": "City parameter is required"})

    @patch('app.services.requests.get')
    @patch('app.services.cache.get')
    @patch('app.services.cache.set')
    def test_recommend_activity_weather_error(self,
                                              mock_cache_get,
                                              mock_requests_get):
        '''Test that an error is returned
        when weather data cannot be fetched'''
        mock_cache_get.return_value = None
        mock_response = Mock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        response = self.client.get('/recommend?city=NonexistentCity')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,
                         {"error": "Unable to fetch weather data"})

    @patch('app.services.requests.get')
    @patch('app.services.suggest_activity')
    @patch('app.services.cache.get')
    @patch('app.services.cache.set')
    def test_recommend_activity_success(self,
                                        mock_cache_get, mock_suggest_activity,
                                        mock_requests_get):
        '''Test that an activity is returned when
        weather data is successfully fetched'''
        mock_cache_get.return_value = None
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 25}
        }
        mock_requests_get.return_value = mock_response
        mock_suggest_activity.return_value = "Go for a picnic"
        response = self.client.get('/recommend?city=London')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"activity": "Go for a picnic"})


if __name__ == '__main__':
    '''Run the tests'''
    unittest.main()
