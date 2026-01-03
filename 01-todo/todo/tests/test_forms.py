from django.test import TestCase
from todo.forms import TodoForm

class TodoFormTest(TestCase):
    def test_valid_form(self):
        data = {'title': 'Test Todo', 'description': 'Desc', 'priority': 'LOW', 'due_date': '2023-12-31'}
        form = TodoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_date(self):
        data = {'title': 'Test Todo', 'due_date': 'invalid-date'}
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_invalid_form(self):
        data = {'title': ''}
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())
