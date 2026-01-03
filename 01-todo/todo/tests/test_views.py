from django.test import TestCase, Client
from django.urls import reverse
from todo.models import Todo

class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo")

    def test_todo_list(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_todo_create(self):
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'New Desc',
            'completed': False,
            'priority': 'MED'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)

    def test_todo_update(self):
        response = self.client.post(reverse('todo_update', args=[self.todo.pk]), {
            'title': 'Updated Todo',
            'description': 'Updated Desc',
            'priority': 'HIGH'
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_todo_delete(self):
        response = self.client.post(reverse('todo_delete', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_todo_toggle(self):
        response = self.client.post(reverse('todo_toggle', args=[self.todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_todo_sorting(self):
        # Create todos with different priorities and due dates
        t1 = Todo.objects.create(title='T1', priority='LOW', due_date='2023-12-01')
        t2 = Todo.objects.create(title='T2', priority='HIGH', due_date='2023-12-01')
        t3 = Todo.objects.create(title='T3', priority='MED', due_date=None)
        t4 = Todo.objects.create(title='T4', priority='HIGH', due_date=None)
        t5 = Todo.objects.create(title='T5', priority='LOW', due_date='2023-11-01')

        response = self.client.get(reverse('todo_list'))
        todos = list(response.context['todos'])

        # Filter out the setup todo for clarity
        todos = [t for t in todos if t.title in ['T1', 'T2', 'T3', 'T4', 'T5']]
        
        self.assertEqual(todos[0].title, 'T5')
        self.assertEqual(todos[1].title, 'T2')
        self.assertEqual(todos[2].title, 'T1')
        self.assertEqual(todos[3].title, 'T4')
        self.assertEqual(todos[4].title, 'T3')
