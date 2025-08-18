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
        response = self.client.get("/full")  # no query param
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing image_id", response.data)

        response = self.client.get("/full", query_string={"image_id": "999999"})
        self.assertEqual(response.status_code, (500))

        # TODO this one does not working, Ayelet is on it.
        # response = self.client.get("/full", query_string={"image_id": "0"})
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.mimetype, "image/jpeg")
        # self.assertTrue(len(response.data) > 0)
        # image = Image.open(io.BytesIO(response.data))
        # image.show()

    #TODO fix this test and add tests with the vakues that should be in the response
    def test_get_image_metadata_success(self):
        valid_image_id = '1'
        response = self.client.get(f'/{valid_image_id}/images-metadata?format=png')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("imagesMetadata", data)
        self.assertIn("imageCount", data)
        self.assertEqual(data["imageCount"], 1)
        self.assertEqual(data["imagesMetadata"][0]["image_id"], str(valid_image_id))
        self.assertEqual(data["imagesMetadata"][0]["imageFormat"], "png")

    def test_get_image_metadata_invalid_id(self):
        invalid_image_id = '-1'
        response = self.client.get(f'/{invalid_image_id}/images-metadata')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("out of bounds", data["message"])

if __name__ == "__main__":
    unittest.main()