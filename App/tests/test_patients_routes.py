import unittest
from flask import Flask
from App.patient.routes import patients_bp
import json

class FilterRouteTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(patients_bp)
        self.client = self.app.test_client()
    
    def check_equal(self, actual, expected):
        for key, expected_value in expected.items():
            self.assertIn(key, actual, f"Key '{key}' missing in response")
            self.assertEqual(actual[key], expected_value)
    def test_filter_images(self):

        filters = {
            "massshape": {"massshape": ["O"]},
            "massmargin": {"massmargin": ["U"]}
        }

        response = self.client.get('/filter', query_string={'filters': json.dumps(filters)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(json.loads(response.data))  # decode twice like your other tests
        self.assertIn(9, data['imageIds'])

        filters = {
            "massmargin": {"massmargin": ["D"]}
        }

        response = self.client.get('/filter', query_string={"filters": json.dumps(filters)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(json.loads(response.data))
        self.assertIn(0, data["imageIds"])
        self.assertIn(1, data["imageIds"])
        self.assertIn(2, data["imageIds"]) 

        filters = {
            "asses": {"asses": ["P"]},
            "calcdistri": {"calcdistri": ["G"]},
            "side": {"side": ["R"]}
        }

        response = self.client.get('/filter', query_string={"filters": json.dumps(filters)})
        self.assertEqual(response.status_code, 200)
        data = json.loads(json.loads(response.data))
        self.assertIn(16, data["imageIds"])
        self.assertIn(17, data["imageIds"])

    def test_filter_images_with_id(self):
        test_image_id = "0"
        response = self.client.get(f"/{test_image_id}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected = {
            'empiAnon': 60696029,
            'accAnon': 8099128854014801,
            'tissueden': 3.0,
            'asses': 'A',
            'side': 'R',
            'massshape': 'S',
            'massmargin': 'D',
            'ViewPosition': 'MLO'
        }
        self.check_equal(data, expected)
        
        test_image_id = "10000000"
        response = self.client.get(f"/{test_image_id}")
        self.assertEqual(response.status_code, 500)

    

if __name__ == '__main__':
    unittest.main()
