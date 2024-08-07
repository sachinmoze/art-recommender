from .models import Artwork, UserProfile, UserInteraction, Exhibition, Preference
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
import numpy as np
import pandas as pd

def get_content_based_recommendations(artwork_id):
    artworks = list(Artwork.objects.all())
    combined_features = [
        ' '.join([
            str(artwork.artist_display) if artwork.artist_display else '',
            str(artwork.medium_display) if artwork.medium_display else '',
            str(artwork.artwork_type_title) if artwork.artwork_type_title else '',
            str(artwork.text_info) if artwork.text_info else '',
            str(artwork.gallery_info) if artwork.gallery_info else '',
            str(artwork.section_info) if artwork.section_info else ''
        ]) for artwork in artworks
    ]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_features)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    idx = next(index for (index, d) in enumerate(artworks) if d.id == artwork_id)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 recommendations
    artwork_indices = [i[0] for i in sim_scores]

    recommended_artworks = [artworks[i] for i in artwork_indices]
    return recommended_artworks

def get_collaborative_recommendations(user_id):
    interactions = UserInteraction.objects.all().values()
    interaction_mapping = {'view': 1, 'like': 2, 'share': 3}
    interaction_df = pd.DataFrame(interactions)
    interaction_df['interaction_type'] = interaction_df['interaction_type'].map(interaction_mapping)

    user_artwork_matrix = pd.pivot_table(interaction_df, index='user_id', columns='artwork_id', values='interaction_type', fill_value=0)
    
    user_item_matrix = user_artwork_matrix.values
    user_item_mean = np.mean(user_item_matrix, axis=1)
    user_item_matrix_normalized = user_item_matrix - user_item_mean.reshape(-1, 1)
    
    k = min(user_item_matrix_normalized.shape) - 1
    if k < 1:
        return []
    
    U, sigma, Vt = svds(user_item_matrix_normalized, k=k)
    sigma = np.diag(sigma)
    
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_item_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings, columns=user_artwork_matrix.columns)
    
    if user_id - 1 >= preds_df.shape[0]:
        return []
    
    user_row_number = user_id - 1
    sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False)
    top_artwork_indices = sorted_user_predictions.head(5).index
    
    recommended_artworks = Artwork.objects.filter(id__in=top_artwork_indices)
    return recommended_artworks

def get_demographic_recommendations(user_profile):
    preferences = [pref.name for pref in user_profile.preferences.all()]
    recommended_artworks = Artwork.objects.filter(artwork_type_title__in=preferences)
    return recommended_artworks

def get_knowledge_based_recommendations(user_profile):
    preferences = [pref.name for pref in user_profile.preferences.all()]
    knowledge_based_recommendations = Artwork.objects.filter(
        artwork_type_title__in=preferences
    )
    return knowledge_based_recommendations

def get_content_based_exhibition_recommendations(user_profile):
    preferences = [pref.name for pref in user_profile.preferences.all()]
    exhibitions = Exhibition.objects.filter(artworks__artwork_type_title__in=preferences).distinct()
    
    combined_features = [
        ' '.join([
            str(exhibition.title),
            str(exhibition.short_description)
        ]).strip() for exhibition in exhibitions
    ]

    # Filter out empty combined features
    combined_features = [doc for doc in combined_features if doc]

    if not combined_features:
        return []

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_features)
    
    user_preferences = ' '.join(preferences).strip()
    if not user_preferences:
        return []

    user_tfidf = tfidf.transform([user_preferences])
    sim_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()
    
    sim_scores = sorted(enumerate(sim_scores), key=lambda x: x[1], reverse=True)
    top_exhibition_indices = [i[0] for i in sim_scores[:5]]

    recommended_exhibitions = [exhibitions[i] for i in top_exhibition_indices]
    return recommended_exhibitions


def get_ensemble_recommendations(user_id, artwork_id):
    content_based_recs = list(get_content_based_recommendations(artwork_id))
    collaborative_recs = list(get_collaborative_recommendations(user_id))
    knowledge_based_recs = list(get_knowledge_based_recommendations(UserProfile.objects.get(user_id=user_id)))
    content_based_exhibition_recs = get_content_based_exhibition_recommendations(UserProfile.objects.get(user_id=user_id))

    combined_recommendations = list(set(content_based_recs + collaborative_recs + knowledge_based_recs))
    return combined_recommendations, content_based_exhibition_recs


def update_recommendations_based_on_feedback(feedback):
    user_id = feedback.get('user_id')
    artwork_id = feedback.get('artwork_id')
    interaction_type = feedback.get('interaction_type')
    
    UserInteraction.objects.create(
        user_id=user_id,
        artwork_id=artwork_id,
        interaction_type=interaction_type
    )
    
    return get_ensemble_recommendations(user_id, artwork_id)

def get_initial_recommendations(user):
    user_profile = UserProfile.objects.get(user=user)
    preferences = [pref.name for pref in user_profile.preferences.all()]
    recommended_artworks = Artwork.objects.filter(artwork_type_title__in=preferences)
    
    return recommended_artworks[:5]
