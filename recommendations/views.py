from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from .models import Artwork, Exhibition, Gallery, Artist, UserProfile, UserInteraction
from .recommendations import (
    get_content_based_recommendations,
    get_collaborative_recommendations,
    get_demographic_recommendations,
    get_knowledge_based_recommendations,
    get_ensemble_recommendations,
    get_initial_recommendations,
    update_recommendations_based_on_feedback
)
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .recommendations import get_content_based_exhibition_recommendations
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponseNotAllowed

def artwork_detail(request, artwork_id):
    try:
        artwork = Artwork.objects.get(id=artwork_id)
        data = {
            'title': artwork.title,
            'artist_display': artwork.artist_display,
            'medium_display': artwork.medium_display,
            'text_info': artwork.text_info,
            'image_url': artwork.image_url
        }
        return JsonResponse(data)
    except Artwork.DoesNotExist:
        return JsonResponse({'error': 'Artwork not found'}, status=404)
    
def all_artworks(request):
    artworks = Artwork.objects.all()
    return render(request, 'recommendations/all_artworks.html', {'artworks': artworks})

def all_exhibitions(request):
    exhibitions = Exhibition.objects.all()
    return render(request, 'recommendations/all_exhibitions.html', {'exhibitions': exhibitions})

def all_artists(request):
    artists = Artist.objects.all()
    return render(request, 'recommendations/all_artists.html', {'artists': artists})

def all_galleries(request):
    galleries = Gallery.objects.all()
    return render(request, 'recommendations/all_galleries.html', {'galleries': galleries})

@csrf_exempt
def conversational_recommendations_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        artwork_id = data.get('artwork_id')
        interaction_type = data.get('interaction_type')
        UserInteraction.objects.create(
            user=request.user,
            artwork_id=artwork_id,
            interaction_type=interaction_type
        )
        return JsonResponse({'status': 'success'})
    initial_recommendations = get_initial_recommendations(request.user)
    return render(request, 'recommendations/conversational_recommend.html', {
        'recommendations': initial_recommendations,
    })
    
def conversational_recommendations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        feedback = {
            'user_id': request.user.id,
            'artwork_id': data.get('artwork_id'),
            'interaction_type': data.get('interaction_type')
        }
        updated_recommendations = update_recommendations_based_on_feedback(feedback)
        print(updated_recommendations)
        artwork_recommendations = [
            {
                'id': rec.id,
                'title': rec.title,
                'artist_display': rec.artist_display,
                'image_url': rec.image_url
            }
            for rec in updated_recommendations[0]
        ]
        exhibition_recommendations = [
            {
                'id': rec.id,
                'title': rec.title,
                'short_description': rec.short_description,
                'image_url': rec.image_url
            }
            for rec in updated_recommendations[1]
        ]
        return JsonResponse({'status': 'success', 'artworks': artwork_recommendations, 'exhibitions': exhibition_recommendations})
    
    initial_recommendations = get_initial_recommendations(request.user)
    return render(request, 'recommendations/conversational_recommend.html', {'recommendations': initial_recommendations})

def index(request):
    artworks = Artwork.objects.all()
    exhibitions = Exhibition.objects.all()
    galleries = Gallery.objects.all()
    artists = Artist.objects.all()
    return render(request, 'recommendations/index.html', {
        'artworks': artworks[:6],
        'exhibitions': exhibitions[:6],
        'galleries': galleries[:6],
        'artists': artists[:6]
    })



def recommend(request, artwork_id):
    content_based_recommendations = get_content_based_recommendations(artwork_id)
    collaborative_recommendations = get_collaborative_recommendations(request.user.id)
    demographic_recommendations = get_demographic_recommendations(request.user.userprofile)
    knowledge_based_recommendations = get_knowledge_based_recommendations(request.user.userprofile)
    ensemble_recommendations, content_based_exhibition_recs = get_ensemble_recommendations(request.user.id, artwork_id)

    return render(request, 'recommendations/recommend.html', {
        'content_based_recommendations': content_based_recommendations,
        'collaborative_recommendations': collaborative_recommendations,
        'demographic_recommendations': demographic_recommendations,
        'knowledge_based_recommendations': knowledge_based_recommendations,
        'ensemble_recommendations': ensemble_recommendations,
        'content_based_exhibition_recs': content_based_exhibition_recs
    })


def ranking_recommendations(request):
    popular_artworks = Artwork.objects.annotate(interaction_count=Count('userinteraction')).order_by('-interaction_count')[:10]
    return render(request, 'recommendations/ranking_recommend.html', {'artworks': popular_artworks})


def exhibition_recommendations(request):
    user_profile = UserProfile.objects.get(user=request.user)
    content_based_exhibition_recs = get_content_based_exhibition_recommendations(user_profile)
    return render(request, 'recommendations/exhibition_recommend.html', {'exhibitions': content_based_exhibition_recs})

def artist_recommendations(request):
    user_profile = UserProfile.objects.get(user=request.user)
    preferences = [pref.name for pref in user_profile.preferences.all()]
    artists = Artist.objects.filter(description__icontains=preferences)
    return render(request, 'recommendations/artist_recommend.html', {'artists': artists})

def popular_artworks(request):
    popular_artworks = Artwork.objects.annotate(interaction_count=Count('userinteraction')).order_by('-interaction_count')[:10]
    return render(request, 'recommendations/popular_artworks.html', {'artworks': popular_artworks})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'profile.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('index')
    return HttpResponseNotAllowed(['POST', 'GET'])
