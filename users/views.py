from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .forms import UserRegisterForm
from content.models import Video

def home(request):
    top = 10

    # Get IDs of videos already shown from the session
    shown_videos = request.session.get('shown_videos', [])
    print("Currently shown videos:", shown_videos)

    # Convert IDs to integers if they are strings
    shown_videos = [int(id) if isinstance(id, str) else id for id in shown_videos]
    
    # Get random videos excluding those already shown
    random_videos = Video.objects.exclude(id__in=shown_videos).order_by('?')[:top]

    # If there aren't enough new videos, reset the list
    if len(random_videos) < top:
        shown_videos = []
        random_videos = Video.objects.all().order_by('?')[:top]
    
    # Get IDs of new videos
    new_video_ids = [video.id for video in random_videos]
    print("New videos to show:", new_video_ids)
    
    # Update the list of shown videos
    new_shown_videos = shown_videos + new_video_ids
    print("New list of shown videos:", new_shown_videos)
    
    # Save to session
    request.session['shown_videos'] = new_shown_videos
    request.session.modified = True  # Ensure the session is saved

    # Get the most popular videos of the month
    popular_videos = Video.get_top_videos_this_month(limit=5)
        
    return render(request, 'users/home.html', {
        'top_videos': random_videos,
        'popular_videos': popular_videos
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
