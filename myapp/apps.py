# myapp/apps.py

from django.apps import AppConfig


class MyappConfig(AppConfig):
    """Configuration class for the 'myapp' Django app.

    Attributes:
        default_auto_field (str): The type of auto-generated primary key field.
        name (str): The name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
