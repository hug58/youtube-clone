from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType

from .forms import VideoForm
from .models import Video, Comment

@login_required
def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            # Extract video ID from embed URL
            embed_url = form.cleaned_data['embed_url']
            url = embed_url.split('src="')[1].split('"')[0]  
            video_id = url.split('/embed/')[1].split('?')[0] 
            video.provider_video_id = video_id
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('home')
    else:
        form = VideoForm()
    
    return render(request, 'content/video_form.html', {'form': form})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    content_type = ContentType.objects.get_for_model(video)
    comments = Comment.objects.filter(content_type=content_type, object_id=video.id).order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'comment' in request.POST:
                comment_text = request.POST.get('comment')
                if comment_text:
                    Comment.objects.create(
                        user=request.user,
                        content_type=content_type,
                        object_id=video.id,
                        content=comment_text
                    )
                    # Update popularity after adding a comment
                    video.calculate_popularity()
                    return redirect('content:video_detail', video_id=video.id)
            elif 'action' in request.POST:
                action = request.POST.get('action')
                if action == 'like':
                    if request.user in video.likes.all():
                        video.likes.remove(request.user)
                    else:
                        video.likes.add(request.user)
                        if request.user in video.dislikes.all():
                            video.dislikes.remove(request.user)
                elif action == 'dislike':
                    if request.user in video.dislikes.all():
                        video.dislikes.remove(request.user)
                    else:
                        video.dislikes.add(request.user)
                        if request.user in video.likes.all():
                            video.likes.remove(request.user)
                
                # Update popularity after like/dislike
                video.calculate_popularity()
                
                # Return the new counts
                return JsonResponse({
                    'likes_count': video.likes.count(),
                    'dislikes_count': video.dislikes.count()
                })

    return render(request, 'content/video_detail.html', {
        'video': video,
        'comments': comments
    })

@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.dislikes.all():
        video.dislikes.remove(request.user)
    video.likes.add(request.user)
    return JsonResponse({
        'likes': video.get_likes_count(),
        'dislikes': video.get_dislikes_count(),
        'likes_percentage': video.get_likes_percentage()
    })

@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
    video.dislikes.add(request.user)
    return JsonResponse({
        'likes': video.get_likes_count(),
        'dislikes': video.get_dislikes_count(),
        'likes_percentage': video.get_likes_percentage()
    })

def popular_videos(request):
    # Get the 5 most popular videos of the month
    top_videos = Video.get_top_videos_this_month(limit=5)
    
    return render(request, 'content/popular_videos.html', {
        'videos': top_videos
    })
