from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend/<int:artwork_id>/', views.recommend, name='recommend'),
    path('ranking_recommendations/', views.ranking_recommendations, name='ranking_recommendations'),
    path('conversational_recommendations/', views.conversational_recommendations, name='conversational_recommendations'),
    path('conversational_recommendations_api/', views.conversational_recommendations_api, name='conversational_recommendations_api'),
    path('exhibition_recommendations/', views.exhibition_recommendations, name='exhibition_recommendations'),
    path('artist_recommendations/', views.artist_recommendations, name='artist_recommendations'),
    path('popular_artworks/', views.popular_artworks, name='popular_artworks'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),  # Added profile URL
    path('logout/', views.user_logout, name='logout'),
    path('api/artworks/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('all_artworks/', views.all_artworks, name='all_artworks'),
    path('all_exhibitions/', views.all_exhibitions, name='all_exhibitions'),
    path('all_artists/', views.all_artists, name='all_artists'),
    path('all_galleries/', views.all_galleries, name='all_galleries'),



]
