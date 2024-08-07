import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from recommendations.models import Artwork, Exhibition, Gallery, Artist, Preference

Artwork.objects.all().delete()
Exhibition.objects.all().delete()
Gallery.objects.all().delete()
Artist.objects.all().delete()
Preference.objects.all().delete()

def fetch_data(url, params=None):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_all_pages(base_url, total_records=1000, params=None):
    all_data = []
    page = 1
    records_fetched = 0
    while records_fetched < total_records:
        if params is None:
            params = {}
        params['page'] = page
        params['limit'] = 100
        data = fetch_data(base_url, params)
        if data and data['data']:
            all_data.extend(data['data'])
            records_fetched += len(data['data'])
            page += 1
            if len(data['data']) < 100:
                break
        else:
            break
    return all_data[:total_records]

def populate_preferences():
    artworks_data = fetch_all_pages('https://api.artic.edu/api/v1/artworks')
    unique_preferences = set()

    for artwork in artworks_data:
        if 'artwork_type_title' in artwork and artwork['artwork_type_title']:
            unique_preferences.add(artwork['artwork_type_title'])

    for preference in unique_preferences:
        Preference.objects.get_or_create(name=preference)

def populate_preferences_from_artworks():
    unique_preferences = Artwork.objects.values_list('artwork_type_title', flat=True).distinct()

    for preference in unique_preferences:
        if preference:
            Preference.objects.get_or_create(name=preference)

def populate_artists():
    artists_data = fetch_all_pages('https://api.artic.edu/api/v1/artists')
    for artist in artists_data:
        Artist.objects.get_or_create(
            name=artist['title'],
            defaults={
                'birth_date': artist.get('birth_date', 'Unknown'),
                'death_date': artist.get('death_date', 'Unknown'),
                'description': artist.get('description', 'No Description')
            }
        )

def populate_artworks():
    artworks_data = fetch_all_pages('https://api.artic.edu/api/v1/artworks')
    for artwork in artworks_data:
        artist, created = Artist.objects.get_or_create(
            name=artwork['artist_display']
        )
        gallery_info = artwork.get('gallery_title', 'Unknown')
        title = artwork['title']
        artist_display = artwork['artist_display']
        medium_display = artwork['medium_display']
        artwork_type_title = artwork['artwork_type_title']
        text_info = artwork.get('description', '')
        section_info = artwork.get('place_of_origin', '')
        image_id = artwork['image_id']
        if image_id:
            image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"
        else:
            image_url = ''
        Artwork.objects.get_or_create(
            title=title,
            defaults={
                'artist_display': artist_display,
                'medium_display': medium_display,
                'artwork_type_title': artwork_type_title,
                'gallery_info': gallery_info,
                'text_info': text_info,
                'section_info': section_info,
                'image_url': image_url,
                'artist': artist
            }
        )

def populate_exhibitions():
    exhibitions_data = fetch_all_pages('https://api.artic.edu/api/v1/exhibitions')
    for exhibition in exhibitions_data:
        if exhibition['status'] != 'Closed':
            start_at = exhibition.get('aic_start_at')
            end_at = exhibition.get('aic_end_at')
            if start_at:
                start_at = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%S%z").date()
            if end_at:
                end_at = datetime.strptime(end_at, "%Y-%m-%dT%H:%M:%S%z").date()
            
            exhibition_obj, created = Exhibition.objects.get_or_create(
                title=exhibition['title'],
                defaults={
                    'short_description': exhibition.get('short_description', ''),
                    'web_url': exhibition.get('web_url',''),
                    'image_url': exhibition.get('image_url',''),
                    'status': exhibition.get('status',''),
                    'start_at': start_at,
                    'end_at': end_at
                }
            )
            
            for artwork_id in exhibition.get('artwork_ids', []):
                try:
                    artwork = Artwork.objects.get(id=artwork_id)
                    exhibition_obj.artworks.add(artwork)
                except Artwork.DoesNotExist:
                    continue

def populate_galleries():
    galleries_data = fetch_all_pages('https://api.artic.edu/api/v1/galleries')
    for gallery in galleries_data:
        Gallery.objects.get_or_create(
            title=gallery['title'],
            defaults={
                'latitude': gallery.get('latitude', 0.0),
                'longitude': gallery.get('longitude', 0.0),
                'floor': gallery.get('floor', 'Unknown')
            }
        )

class Command(BaseCommand):
    help = 'Populate the database with data from the Art Institute of Chicago API'

    def handle(self, *args, **kwargs):
        populate_artworks()
        self.stdout.write(self.style.SUCCESS('Successfully populated the artworks'))
        populate_exhibitions()
        self.stdout.write(self.style.SUCCESS('Successfully populated the exhibitions'))
        populate_galleries()
        self.stdout.write(self.style.SUCCESS('Successfully populated the galleries'))
        populate_artists()
        self.stdout.write(self.style.SUCCESS('Successfully populated the artists'))
        #populate_preferences()
        populate_preferences_from_artworks()
        self.stdout.write(self.style.SUCCESS('Successfully populated the preferences'))
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
