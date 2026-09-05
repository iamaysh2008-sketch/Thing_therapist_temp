import io
import os
import unittest
from unittest.mock import patch

import app
from openai import AuthenticationError


class FakeMessage:
    content = "OBJECT: Chair\nADVICE: Take a stand."


class FakeChoice:
    message = FakeMessage()


class FakeResponse:
    choices = [FakeChoice()]


class FakeCompletions:
    def __init__(self):
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.completions = FakeCompletions()
        self.chat = type("Chat", (), {"completions": self.completions})()


class AppTests(unittest.TestCase):
    def test_analyser_sends_openrouter_vision_request(self):
        fake_client = FakeClient()

        with patch.object(app, "get_openai_client", return_value=fake_client):
            response = app.app.test_client().post(
                "/analyser",
                data={"image": (io.BytesIO(b"image-bytes"), "chair.jpg")},
                content_type="multipart/form-data",
            )

        request = fake_client.completions.request
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request["model"], "openai/gpt-4o-mini")
        self.assertEqual(request["messages"][0]["content"][0]["type"], "text")
        image_part = request["messages"][0]["content"][1]
        self.assertEqual(image_part["type"], "image_url")
        self.assertTrue(image_part["image_url"]["url"].startswith("data:image/jpeg;base64,"))
        self.assertIn("OBJECT: Chair", response.get_data(as_text=True))

    def test_authentication_error_is_shown_to_user(self):
        error = AuthenticationError(
            message="invalid key",
            response=type(
                "Response",
                (),
                {
                    "request": None,
                    "status_code": 401,
                    "headers": {},
                },
            )(),
            body={"error": {"message": "invalid key"}},
        )

        with patch.object(app, "get_openai_client", side_effect=error):
            response = app.app.test_client().post(
                "/analyser",
                data={"image": (io.BytesIO(b"image-bytes"), "chair.jpg")},
                content_type="multipart/form-data",
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("OPENROUTER_API_KEY", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
