import unittest
from flask import Flask
from App.patient.routes import patients_bp
import json

class FilterRouteTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(patients_bp)
        self.client = self.app.test_client()

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
    

if __name__ == '__main__':
    unittest.main()
