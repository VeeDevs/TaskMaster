# myapp/views.py

from django.shortcuts import render
from .models import Band, Album


def home(request):
    """View function for the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'home.html' template.
    """
    return render(request, 'home.html')


def band_list(request):
    """View function for displaying a list of bands.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'band_list.html' template with the list of bands.
    """
    bands = Band.objects.all()
    return render(request, 'band_list.html', {'bands': bands})


def album_list(request):
    """View function for displaying a list of albums.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 'album_list.html' template with the list of albums.
    """
    albums = Album.objects.all()
    return render(request, 'album_list.html', {'albums': albums})
