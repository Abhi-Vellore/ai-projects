from django.db import models

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MED', 'Medium'),
        ('LOW', 'Low'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='MED')
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
