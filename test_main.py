import unittest
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
from main import print_menu


class TestMain(unittest.TestCase):
    """Test cases for the main module."""

    @patch("builtins.print")
    def test_print_menu(self, mock_print):
        """Test that the menu is printed correctly."""
        print_menu()

        # Verify that print was called multiple times
        self.assertGreater(mock_print.call_count, 0)
        
        # Verify specific menu items are printed
        printed_text = " ".join([str(call) for call in mock_print.call_args_list])
        self.assertIn("Task Manager", printed_text)
        self.assertIn("Add task", printed_text)
        self.assertIn("Exit", printed_text)

    @patch("builtins.print")
    def test_print_menu_options_count(self, mock_print):
        """Test that all menu options are printed."""
        print_menu()

        # Should print title and at least 6 options
        self.assertGreaterEqual(mock_print.call_count, 7)


if __name__ == "__main__":
    unittest.main()
