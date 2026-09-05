import io
import os
import unittest
from unittest.mock import patch

import app


class FakeMessage:
    content = "OBJECT: Chair\nADVICE: Take a stand."


class FakeChoice:
    message = FakeMessage()


class FakeResponse:
    choices = [FakeChoice()]


class FakeModels:
    def __init__(self):
        self.request = None

    def generate_content(self, **kwargs):
        self.request = kwargs
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


class AppTests(unittest.TestCase):
    def test_analyser_sends_gemini_vision_request(self):
        fake_client = FakeClient()

        with patch.object(app, "get_gemini_client", return_value=fake_client):
            response = app.app.test_client().post(
                "/analyser",
                data={"image": (io.BytesIO(b"image-bytes"), "chair.jpg")},
                content_type="multipart/form-data",
            )

        request = fake_client.models.request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request["model"], "gemini-2.5-flash")
        self.assertIn("OBJECT:", request["contents"][0])
        image_part = request["contents"][1]
        self.assertEqual(image_part.mime_type, "image/jpeg")
        self.assertEqual(image_part.data, b"image-bytes")
        self.assertIn("OBJECT: Chair", response.get_data(as_text=True))

    def test_authentication_error_is_shown_to_user(self):
        error = RuntimeError("invalid API key")

        with patch.object(app, "get_gemini_client", side_effect=error):
            response = app.app.test_client().post(
                "/analyser",
                data={"image": (io.BytesIO(b"image-bytes"), "chair.jpg")},
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("GEMINI_API_KEY", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
