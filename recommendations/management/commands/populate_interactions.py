import random
import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand
from recommendations.models import UserProfile, Artwork, UserInteraction

class Command(BaseCommand):
    help = 'Generating dummy user interactions into the database'

    def handle(self, *args, **kwargs):
        self.generate_dummy_interactions()
        self.stdout.write(self.style.SUCCESS('Dummy interactions created successfully!'))

    def generate_dummy_interactions(self):
        user_profiles = UserProfile.objects.all()
        artworks = Artwork.objects.all()

        user_ids = list(user_profiles.values_list('user_id', flat=True))
        artwork_ids = list(artworks.values_list('id', flat=True))

        interaction_types = ['view', 'like', 'share']

        num_interactions = 1000
        dummy_interactions = []

        for _ in range(num_interactions):
            interaction_type = random.choice(interaction_types)
            user_id = random.choice(user_ids)
            artwork_id = random.choice(artwork_ids)
            timestamp = datetime.now()

            dummy_interactions.append(UserInteraction(
                user_id=user_id,
                artwork_id=artwork_id,
                interaction_type=interaction_type,
                timestamp=timestamp
            ))

        UserInteraction.objects.bulk_create(dummy_interactions)
