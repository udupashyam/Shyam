import unittest
from unittest.mock import patch
from app import flask_app as app, fetch_info, PERSONAL_INFO_URL

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    @patch('requests.get')
    def test_index_mobile_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'd': {'results': [{'personIdExternal': '12345'}]}
        }
        response = self.client.post('/', data={'mobile': '9876543210'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome 12345', response.data)

    @patch('requests.get')
    def test_index_mobile_not_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'d': {'results': []}}
        response = self.client.post('/', data={'mobile': '0000000000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phone number cannot be found. Contact your HR.', response.data)

    @patch('requests.get')
    def test_fetch_info_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'mock': 'data'}
        with app.test_request_context():
            response = fetch_info(PERSONAL_INFO_URL, '12345', 'Personal Information')
            self.assertIn('mock', response)

if __name__ == '__main__':
    unittest.main()
