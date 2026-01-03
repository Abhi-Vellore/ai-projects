from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Case, When, Value, IntegerField, F
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    # Sort by:
    # 1. Due Date (Ascending, Nulls Last - achieved by sorting by F('due_date').asc(nulls_last=True))
    # 2. Priority (High=1, Med=2, Low=3)
    
    todos = Todo.objects.annotate(
        priority_val=Case(
            When(priority='HIGH', then=Value(1)),
            When(priority='MED', then=Value(2)),
            When(priority='LOW', then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by(F('due_date').asc(nulls_last=True), 'priority_val')
    
    filter_status = request.GET.get('filter', 'all')
    if filter_status == 'active':
        todos = todos.filter(completed=False)
    elif filter_status == 'done':
        todos = todos.filter(completed=True)
        
    return render(request, 'todo/todo_list.html', {'todos': todos, 'filter': filter_status})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo/todo_confirm_delete.html', {'todo': todo})

@require_POST
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
