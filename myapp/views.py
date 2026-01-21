# myapp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task, Comment, UserProfile, Tag
from .forms import TaskForm, CommentForm, UserRegistrationForm


def register(request):
    """View function for user registration.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'registration/register.html' template.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is auto-created by signal, no need to create manually
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def home(request):
    """View function for the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'home.html' template.
    """
    if request.user.is_authenticated:
        tasks_count = Task.objects.filter(owner=request.user).count()
        assigned_count = Task.objects.filter(assignee=request.user).count()
        context = {
            'tasks_count': tasks_count,
            'assigned_count': assigned_count,
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html')


@login_required
def task_list(request):
    """View function for displaying a list of tasks.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'task_list.html' template with tasks.
    """
    tasks = Task.objects.filter(owner=request.user)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)
    
    # Search
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    context = {
        'tasks': tasks,
        'statuses': Task.STATUS_CHOICES,
        'priorities': Task.PRIORITY_CHOICES,
    }
    return render(request, 'task_list.html', context)


@login_required
def assigned_tasks(request):
    """View function for displaying tasks assigned to the user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'assigned_tasks.html' template.
    """
    tasks = Task.objects.filter(assignee=request.user)
    
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    context = {
        'tasks': tasks,
        'statuses': Task.STATUS_CHOICES,
    }
    return render(request, 'assigned_tasks.html', context)


@login_required
def task_detail(request, pk):
    """View function for displaying task details.

    Args:
        request: The HTTP request object.
        pk: Primary key of the task.

    Returns:
        HttpResponse: The rendered 'task_detail.html' template.
    """
    task = get_object_or_404(Task, pk=pk)
    
    # Check if user has permission to view this task
    if task.owner != request.user and task.assignee != request.user:
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('task_list')
    
    comments = task.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = CommentForm()
    
    context = {
        'task': task,
        'comments': comments,
        'form': form,
    }
    return render(request, 'task_detail.html', context)


@login_required
def task_create(request):
    """View function for creating a new task.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'task_form.html' template.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    
    context = {'form': form}
    return render(request, 'task_form.html', context)


@login_required
def task_update(request, pk):
    """View function for updating a task.

    Args:
        request: The HTTP request object.
        pk: Primary key of the task.

    Returns:
        HttpResponse: The rendered 'task_form.html' template.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if task.owner != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    context = {'form': form, 'task': task}
    return render(request, 'task_form.html', context)


@login_required
def task_delete(request, pk):
    """View function for deleting a task.

    Args:
        request: The HTTP request object.
        pk: Primary key of the task.

    Returns:
        HttpResponse: Redirect to task_list after deletion.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if task.owner != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'task_confirm_delete.html', context)


@login_required
def user_profile(request, username):
    """View function for displaying user profile.

    Args:
        request: The HTTP request object.
        username: Username of the profile to display.

    Returns:
        HttpResponse: The rendered 'profile.html' template.
    """
    user = get_object_or_404(User, username=username)
    # Ensure user has a profile (create if missing)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    tasks = Task.objects.filter(owner=user)
    context = {
        'profile': profile,
        'tasks': tasks,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    """View function for editing user profile.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'edit_profile.html' template.
    """
    # Ensure user has a profile (create if missing)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')
        
        profile.bio = bio
        if avatar:
            profile.avatar = avatar
        profile.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile', username=request.user.username)
    
    context = {'profile': profile}
    return render(request, 'edit_profile.html', context)
