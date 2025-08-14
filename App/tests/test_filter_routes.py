import unittest
from flask import Flask
from App.filter.routes import filter_bp
import json

class FilterRouteTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(filter_bp)
        self.client = self.app.test_client()

    def check_equality(self, data, expected_data):
        for key, expected_values in expected_data.items():
            self.assertIn(key, data)
            self.assertEqual(set(data[key]), set(expected_values))

    def test_filter_options_route(self):
        response = self.client.get('/options')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
        data = json.loads(json.loads(response.data)) 

        expected_data = {
            "asses": ["A", "B", "K", "M", "N", "P", "S", "X"], 
            "side": ["B", "L", "R"], 
            "massdens": ["+", "-", "0", "="], 
            "type": ["B", "S"], 
            "pathSeverity": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
            "ViewPosition": ['MLO', 'CC', 'XCCL', 'ML', 'LM', 'CV', 'XCCM', 'RL', 'RM',
                 'AT', 'FB', 'TAN', 'CCID', 'MLOID', 'SIO', 'MLID', 
                 'SPECIMEN', 'LMO', 'LMID']
        }

        self.check_equality(data, expected_data)
    
    def test_abnormality_options_route(self):
        response = self.client.get('/abnormality-options')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
        data = json.loads(json.loads(response.data))

        expected_data = {
            "tissueden": [1.0, 2.0, 3.0, 4.0, 5.0],
            "massshape": ["S", "F", "O", "G", "B", "L", "R", "A", "X", "Q", "N", "Y", "V", "T", "M"],
            "massmargin": ["D", "U", "I", "S", "M"],
            "calcdistri": ['G', 'R', 'C', 'D', 'S', 'L']
        }
        
        self.check_equality(data, expected_data)

    def test_numbers_endpoint(self):
        response = self.client.get('/image-ids')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
        data = json.loads(json.loads(response.data))  # decode JSON if double-encoded
        image_ids = set(data["imageIds"])  # convert to set to ignore order
        expected_ids = set(range(0, 152607))  
        self.assertEqual(image_ids, expected_ids)


if __name__ == '__main__':
    unittest.main()

