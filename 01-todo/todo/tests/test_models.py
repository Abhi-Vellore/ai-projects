from django.test import TestCase
from todo.models import Todo

class TodoModelTest(TestCase):
    def test_create_todo(self):
        todo = Todo.objects.create(title="Test Todo", description="Test Description", priority='HIGH')
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertFalse(todo.completed)
        self.assertTrue(todo.created_at)
        self.assertEqual(todo.priority, 'HIGH')
        self.assertIsNone(todo.due_date)

    def test_default_priority(self):
        todo = Todo.objects.create(title="Default Priority")
        self.assertEqual(todo.priority, 'MED')

    def test_str_representation(self):
        todo = Todo.objects.create(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")
