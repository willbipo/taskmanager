import unittest
from unittest.mock import patch, MagicMock
from ai_service import create_simple_tasks


class TestAIService(unittest.TestCase):
    """Test cases for the AI service module."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_success(self, mock_client):
        """Test successfully creating subtasks from description."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """- Subtask 1
- Subtask 2
- Subtask 3"""
        mock_client.chat.completions.create.return_value = mock_response

        result = create_simple_tasks("Complex task description")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Subtask 1")
        self.assertEqual(result[1], "Subtask 2")
        self.assertEqual(result[2], "Subtask 3")
        mock_client.chat.completions.create.assert_called_once()

    @patch.dict("os.environ", {"OPENAI_API_KEY": ""})
    def test_create_simple_tasks_no_api_key(self):
        """Test creating tasks when API key is not configured."""
        with patch("ai_service.client.api_key", ""):
            result = create_simple_tasks("Task description")
            self.assertEqual(result, ["Error: La API key de OpenAI no está configurada."])

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_api_error(self, mock_client):
        """Test handling of API connection errors."""
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_client.api_key = "test-key-123"

        result = create_simple_tasks("Task description")

        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].startswith("Error de conexión o parámetros:"))

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_empty_response(self, mock_client):
        """Test handling of empty API response."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = ""
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key-123"

        result = create_simple_tasks("Task description")

        self.assertEqual(result, ["Error: No se han podido generar las subtareas."])

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_with_extra_whitespace(self, mock_client):
        """Test parsing subtasks with extra whitespace."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """  - Subtask 1  
- Subtask 2
  -  Subtask 3  """
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key-123"

        result = create_simple_tasks("Task description")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "Subtask 1")
        self.assertEqual(result[1], "Subtask 2")
        self.assertEqual(result[2], "Subtask 3")

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_multiple_subtasks(self, mock_client):
        """Test creating multiple subtasks (3-5 range)."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """- Subtask 1
- Subtask 2
- Subtask 3
- Subtask 4
- Subtask 5"""
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key-123"

        result = create_simple_tasks("Complex task")

        self.assertEqual(len(result), 5)
        for i, subtask in enumerate(result, 1):
            self.assertEqual(subtask, f"Subtask {i}")

    @patch.dict("os.environ", {"OPENAI_API_KEY": "test-key-123"})
    @patch("ai_service.client")
    def test_create_simple_tasks_prompt_content(self, mock_client):
        """Test that the prompt is correctly formatted."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "- Task 1"
        mock_client.chat.completions.create.return_value = mock_response
        mock_client.api_key = "test-key-123"

        description = "Test description for task"
        create_simple_tasks(description)

        # Verify the API was called with the correct structure
        call_args = mock_client.chat.completions.create.call_args
        self.assertIsNotNone(call_args)
        self.assertEqual(call_args.kwargs["model"], "gpt-5.4-mini")
        self.assertEqual(call_args.kwargs["max_completion_tokens"], 300)
        self.assertEqual(call_args.kwargs["reasoning_effort"], "low")


if __name__ == "__main__":
    unittest.main()
