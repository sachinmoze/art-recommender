from sklearn.metrics import precision_score, recall_score, f1_score

from recommendations.recommendations import get_initial_recommendations
from .models import UserInteraction, Artwork, UserProfile
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

def get_true_labels(user_id):
    interactions = UserInteraction.objects.filter(user_id=user_id)
    true_labels = set(interactions.values_list('artwork_id', flat=True))
    return true_labels

def get_predicted_labels(user_id, recommendations):
    predicted_labels = set(recommendation.id for recommendation in recommendations)
    return predicted_labels

def evaluate_recommendations(user_id, recommendations):
    true_labels = get_true_labels(user_id)
    predicted_labels = get_predicted_labels(user_id, recommendations)

    y_true = [1 if artwork_id in true_labels else 0 for artwork_id in predicted_labels]
    y_pred = [1] * len(predicted_labels)

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return precision, recall, f1

def evaluate_all_users():
    users = UserInteraction.objects.values_list('user_id', flat=True).distinct()
    all_precision = []
    all_recall = []
    all_f1 = []

    for user_id in users:
        user_profile = UserProfile.objects.get(user_id=user_id)
        initial_recommendations = get_initial_recommendations(user_profile.user)
        precision, recall, f1 = evaluate_recommendations(user_id, initial_recommendations)
        all_precision.append(precision)
        all_recall.append(recall)
        all_f1.append(f1)

    avg_precision = np.mean(all_precision)
    avg_recall = np.mean(all_recall)
    avg_f1 = np.mean(all_f1)

    return avg_precision, avg_recall, avg_f1
