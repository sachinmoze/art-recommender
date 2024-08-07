from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=255, null=True, blank=True)
    death_date = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    artist_display = models.CharField(max_length=255, null=True, blank=True)
    medium_display = models.CharField(max_length=255, null=True, blank=True)
    artwork_type_title = models.CharField(max_length=255, null=True, blank=True)
    gallery_info = models.CharField(max_length=255, null=True, blank=True)
    text_info = models.TextField(null=True, blank=True)
    section_info = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Exhibition(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    web_url = models.URLField(max_length=255, null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    artworks = models.ManyToManyField(Artwork, related_name='exhibitions')  # Link to artworks

    def __str__(self):
        return self.title

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Preference(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.ManyToManyField(Preference, blank=True,null=True)

    def __str__(self):
        return self.user.username

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., 'view', 'like', 'share'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.artwork.title} - {self.interaction_type}"
