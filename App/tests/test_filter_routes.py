import unittest
from flask import Flask
from App.filter.routes import filter_bp
import json

class FilterOptionsTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(filter_bp)
        self.client = self.app.test_client()

    def test_filter_options_route(self):
        response = self.client.get('/options')
        data = json.loads(json.loads(response.data))  # decode twice in one line
        print("Response data:", data)

        expected_data = {
            "asses": ["A", "B", "K", "M", "N", "P", "S", "X"], 
            "side": ["B", "L", "R"], 
            "massdens": ["+", "-", "0", "="], 
            "type": ["B", "S"], 
            "pathSeverity": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
        }

        for key, expected_values in expected_data.items():
            self.assertIn(key, data)
            self.assertEqual(set(data[key]), set(expected_values))

if __name__ == '__main__':
    unittest.main()
