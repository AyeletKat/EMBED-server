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

    # TODO
    def test_images_metadata(self):
        response = self.client.get("/images-metadata")