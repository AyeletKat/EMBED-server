import unittest
from flask import Flask
from App.image.routes import images_bp
import json
from PIL import Image
import io

class FilterRouteTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(images_bp)
        self.client = self.app.test_client()
    
    def test_full(self):
        image_id = 999999
        response = self.client.get(f"/{image_id}/full")
        self.assertEqual(response.status_code, 400)
        
        image_id = -1
        response = self.client.get(f"/{image_id}/full")
        self.assertEqual(response.status_code, 400)

        image_id = 16
        response = self.client.get(f"/{image_id}/full")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/png")
        self.assertTrue(len(response.data) > 0)
        image = Image.open(io.BytesIO(response.data))
        image.show()

    def test_get_image_metadata_success(self):
        valid_image_id = '2'
        response = self.client.get(f'/{valid_image_id}/images-metadata?format=png')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["imageFormat"], "png")
    
    def test_get_image_metadata(self):
        image_id = 1
        response = self.client.get(f"/{image_id}/images-metadata?format=png")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        expected = {
            "FinalImageType": "2D",
            "SeriesDescription": "R MLO",
            "ViewPosition": "MLO",
            "imageFormat": "png",
            "image_id": "1",
            "side": "R"
        }
        self.assertEqual(data, expected)

    def test_get_image_metadata_invalid_id(self):
        invalid_image_id = '-1'
        response = self.client.get(f'/{invalid_image_id}/images-metadata?format=png')
        self.assertEqual(response.status_code, 400)
        body = response.get_data(as_text=True)
        self.assertIn("Image ID -1 is out of bounds", body)

if __name__ == "__main__":
    unittest.main()