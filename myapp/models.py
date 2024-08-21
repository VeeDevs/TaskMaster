# myapp/models.py

from django.db import models


class Band(models.Model):
    """Model representing a musical band.

    Attributes:
        name (str): The name of the band.
        genre (str): The genre of music the band plays.
    """

    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

    def __str__(self):
        """String representation of the Band model."""
        return self.name


class Album(models.Model):
    """Model representing a musical album.

    Attributes:
        band (Band): The band that released the album.
        title (str): The title of the album.
        release_date (date): The release date of the album.
    """

    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        """String representation of the Album model."""
        return self.title
