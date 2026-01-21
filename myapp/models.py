# myapp/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Model representing user profile with additional information.

    Attributes:
        user (User): The Django User model.
        bio (str): A short biography of the user.
        avatar (ImageField): User's profile picture.
        created_at (datetime): When the profile was created.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the UserProfile model."""
        return f"{self.user.username}'s Profile"


class Task(models.Model):
    """Model representing a task.

    Attributes:
        title (str): The title of the task.
        description (str): Detailed description of the task.
        owner (User): The user who created the task.
        assignee (User): The user assigned to complete the task.
        priority (str): Priority level of the task.
        status (str): Current status of the task.
        due_date (date): When the task is due.
        created_at (datetime): When the task was created.
        updated_at (datetime): When the task was last updated.
    """

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks'
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """String representation of the Task model."""
        return self.title


class Comment(models.Model):
    """Model representing a comment on a task.

    Attributes:
        task (Task): The task being commented on.
        author (User): The user who made the comment.
        content (str): The comment text.
        created_at (datetime): When the comment was created.
        updated_at (datetime): When the comment was last updated.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        """String representation of the Comment model."""
        return f"Comment by {self.author.username} on {self.task.title}"


class Tag(models.Model):
    """Model representing a tag for tasks.

    Attributes:
        name (str): The name of the tag.
        description (str): Description of the tag.
        tasks (Task): Many-to-many relationship with tasks.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Tag model."""
        return self.name

    class Meta:
        ordering = ['name']


class TaskTag(models.Model):
    """Model representing the relationship between tasks and tags.

    Attributes:
        task (Task): The task.
        tag (Tag): The tag.
        created_at (datetime): When the relationship was created.
    """

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='tags_through')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'tag')

    def __str__(self):
        """String representation of the TaskTag model."""
        return f"{self.task.title} - {self.tag.name}"

# Django signals for auto-creation
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()