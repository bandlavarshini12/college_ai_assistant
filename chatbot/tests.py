import json
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from .views import build_general_answer, get_gemini_answer


class GeneralAssistantTests(SimpleTestCase):
    def test_python_question(self):
        answer = build_general_answer("What is Python?")
        self.assertIn("Python", answer)
        self.assertIn("programming", answer.lower())

    def test_study_question(self):
        answer = build_general_answer("How can I improve my study habits?")
        self.assertIn("study", answer.lower())

    def test_general_fallback(self):
        answer = build_general_answer("Tell me about AI and machine learning")
        self.assertTrue("AI" in answer or "artificial" in answer.lower())
        self.assertTrue("machine learning" in answer.lower() or "learning" in answer.lower())

    @patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"}, clear=True)
    @patch("chatbot.views.request.urlopen")
    def test_gemini_answer_uses_key_and_extracts_text(self, urlopen):
        response = MagicMock()
        response.read.return_value = json.dumps(
            {
                "candidates": [
                    {"content": {"parts": [{"text": "A verified answer."}]}}
                ]
            }
        ).encode("utf-8")
        urlopen.return_value.__enter__.return_value = response

        answer = get_gemini_answer("What is machine learning?")

        self.assertEqual(answer, "A verified answer.")
        api_request = urlopen.call_args.args[0]
        self.assertEqual(api_request.headers["X-goog-api-key"], "test-key")
        self.assertIn(b"google_search", api_request.data)
