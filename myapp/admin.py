from django.contrib import admin
from .models import Task, Comment, UserProfile, Tag, TaskTag


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""
    list_display = ('title', 'owner', 'assignee', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'owner__username', 'assignee__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description'),
        }),
        ('Assignment', {
            'fields': ('owner', 'assignee'),
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority'),
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at'),
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for Comment model."""
    list_display = ('author', 'task', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'task__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for Tag model."""
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    """Admin configuration for TaskTag model."""
    list_display = ('task', 'tag', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'tag__name')
    readonly_fields = ('created_at',)
