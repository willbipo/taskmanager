import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def test_task_creation(self):
        """Test creating a Task instance."""
        task = Task(1, "Buy groceries", "Get milk and eggs")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.name, "Buy groceries")
        self.assertEqual(task.description, "Get milk and eggs")
        self.assertFalse(task.completed)

    def test_task_creation_with_completed(self):
        """Test creating a completed Task."""
        task = Task(2, "Write report", "Complete quarterly report", True)
        self.assertTrue(task.completed)

    def test_task_str_representation_incomplete(self):
        """Test string representation of incomplete task."""
        task = Task(1, "Buy groceries", "Get milk and eggs")
        expected = "[ ] #1: Buy groceries"
        self.assertEqual(str(task), expected)

    def test_task_str_representation_complete(self):
        """Test string representation of complete task."""
        task = Task(1, "Buy groceries", "Get milk and eggs", True)
        expected = "[✓] #1: Buy groceries"
        self.assertEqual(str(task), expected)


class TestTaskManager(unittest.TestCase):
    """Test cases for the TaskManager class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        # Mock file operations to avoid actual file I/O
        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=[]):
                self.manager = TaskManager()

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_add_single_task(self, mock_save, mock_print):
        """Test adding a single task."""
        self.manager.add_task("Buy groceries", "Get milk and eggs")

        self.assertEqual(len(self.manager._tasks), 1)
        task = self.manager._tasks[0]
        self.assertEqual(task.name, "Buy groceries")
        self.assertEqual(task.description, "Get milk and eggs")
        self.assertEqual(task.id, 1)
        self.assertFalse(task.completed)
        mock_save.assert_called_once()
        mock_print.assert_called_with("Task added: Buy groceries")

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_add_multiple_tasks(self, mock_save, mock_print):
        """Test adding multiple tasks with correct id increments."""
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        self.manager.add_task("Task 3", "Description 3")

        self.assertEqual(len(self.manager._tasks), 3)
        self.assertEqual(self.manager._tasks[0].id, 1)
        self.assertEqual(self.manager._tasks[1].id, 2)
        self.assertEqual(self.manager._tasks[2].id, 3)
        self.assertEqual(self.manager._next_id, 4)
        self.assertEqual(mock_save.call_count, 3)

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_list_tasks_with_tasks(self, mock_save, mock_print):
        """Test listing tasks when tasks exist."""
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        
        mock_print.reset_mock()
        self.manager.list_task()

        # Should print each task
        calls = mock_print.call_args_list
        self.assertEqual(len(calls), 2)

    @patch("builtins.print")
    def test_list_tasks_empty(self, mock_print):
        """Test listing tasks when no tasks exist."""
        self.manager.list_task()
        mock_print.assert_called_with("Tasks not found")

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_complete_task_existing(self, mock_save, mock_print):
        """Test completing an existing task."""
        self.manager.add_task("Task 1", "Description 1")
        
        mock_print.reset_mock()
        mock_save.reset_mock()
        
        self.manager.complete_task(1)

        self.assertTrue(self.manager._tasks[0].completed)
        mock_save.assert_called_once()
        mock_print.assert_called_with("Task completed: Task 1")

    @patch("builtins.print")
    def test_complete_task_nonexistent(self, mock_print):
        """Test completing a non-existent task."""
        self.manager.complete_task(999)
        mock_print.assert_called_with("Task not found: 999")

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_delete_task_existing(self, mock_save, mock_print):
        """Test deleting an existing task."""
        self.manager.add_task("Task 1", "Description 1")
        
        mock_print.reset_mock()
        mock_save.reset_mock()
        
        self.manager.delete_task(1)

        self.assertEqual(len(self.manager._tasks), 0)
        mock_save.assert_called_once()
        mock_print.assert_called_with("Task removed: 1")

    @patch("builtins.print")
    def test_delete_task_nonexistent(self, mock_print):
        """Test deleting a non-existent task."""
        self.manager.delete_task(999)
        mock_print.assert_called_with("Task not found: 999")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_tasks_from_file(self, mock_json_load, mock_file):
        """Test loading tasks from a file."""
        mock_data = [
            {"id": 1, "name": "Task 1", "description": "Desc 1", "completed": False},
            {"id": 2, "name": "Task 2", "description": "Desc 2", "completed": True},
        ]
        mock_json_load.return_value = mock_data

        manager = TaskManager()

        self.assertEqual(len(manager._tasks), 2)
        self.assertEqual(manager._tasks[0].name, "Task 1")
        self.assertEqual(manager._tasks[1].name, "Task 2")
        self.assertTrue(manager._tasks[1].completed)
        self.assertEqual(manager._next_id, 3)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_load_tasks_file_not_found(self, mock_json_load, mock_file):
        """Test loading tasks when file doesn't exist."""
        mock_file.side_effect = FileNotFoundError()

        manager = TaskManager()

        self.assertEqual(len(manager._tasks), 0)
        self.assertEqual(manager._next_id, 1)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    @patch.object(TaskManager, "load_tasks")
    def test_save_tasks_to_file(self, mock_load, mock_json_dump, mock_file):
        """Test saving tasks to a file."""
        manager = TaskManager()
        manager._tasks = [
            Task(1, "Task 1", "Desc 1", False),
            Task(2, "Task 2", "Desc 2", True),
        ]

        manager.save_tasks()

        mock_file.assert_called_with("tasks.json", "w")
        mock_json_dump.assert_called_once()
        
        # Verify the data structure passed to json.dump
        called_data = mock_json_dump.call_args[0][0]
        self.assertEqual(len(called_data), 2)
        self.assertEqual(called_data[0]["name"], "Task 1")
        self.assertEqual(called_data[1]["completed"], True)

    @patch("builtins.print")
    @patch.object(TaskManager, "save_tasks")
    def test_next_id_increments(self, mock_save, mock_print):
        """Test that _next_id increments correctly."""
        initial_id = self.manager._next_id
        self.manager.add_task("Task 1", "Description 1")
        self.assertEqual(self.manager._next_id, initial_id + 1)
        
        self.manager.add_task("Task 2", "Description 2")
        self.assertEqual(self.manager._next_id, initial_id + 2)


if __name__ == "__main__":
    unittest.main()
