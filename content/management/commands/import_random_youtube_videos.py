from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import Video
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random
import os
from datetime import datetime
import time
from django.utils import timezone

# Keywords for random searches
SEARCH_KEYWORDS = [
    "tutorial", "how to", "programming", "coding", "technology",
    "science", "education", "learning", "development", "software",
    "web development", "python", "javascript", "django", "react",
    "computer science", "data science", "machine learning", "AI",
    "gaming", "music", "art", "design", "photography", "travel"
]

class Command(BaseCommand):
    help = 'Import random YouTube videos using YouTube Data API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of videos to import'
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Username of the user who will upload the videos'
        )
        parser.add_argument(
            '--api-key',
            type=str,
            help='YouTube Data API key'
        )

    def handle(self, *args, **options):
        count = options['count']
        username = options['user']
        api_key = options['api_key'] or os.getenv('YOUTUBE_API_KEY')

        if not api_key:
            self.stdout.write(self.style.ERROR('Please provide a YouTube API key with --api-key or set YOUTUBE_API_KEY environment variable'))
            return

        if not username:
            self.stdout.write(self.style.ERROR('Please provide a username with --user'))
            return

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return

        # Create the YouTube service
        youtube = build('youtube', 'v3', developerKey=api_key)

        videos_imported = 0
        while videos_imported < count:
            try:
                # Select a random keyword
                keyword = random.choice(SEARCH_KEYWORDS)
                
                # Perform the search
                search_response = youtube.search().list(
                    q=keyword,
                    part='id,snippet',
                    maxResults=50,
                    type='video',
                    videoDuration='medium',  # Medium duration videos
                    relevanceLanguage='en',  # English videos
                    order='viewCount'  # Sort by view count
                ).execute()

                # Process the results
                for search_result in search_response.get('items', []):
                    if videos_imported >= count:
                        break

                    video_id = search_result['id']['videoId']
                    
                    # Get video details
                    video_response = youtube.videos().list(
                        part='snippet',
                        id=video_id
                    ).execute()

                    if not video_response['items']:
                        continue

                    video_details = video_response['items'][0]
                    snippet = video_details['snippet']

                    # Check if the video already exists
                    if Video.objects.filter(provider_video_id=video_id).exists():
                        continue

                    # Convert publication date to datetime
                    published_at = datetime.strptime(
                        snippet['publishedAt'], 
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                    published_at = timezone.make_aware(published_at)

                    # Create the video
                    video = Video.objects.create(
                        title=snippet['title'],
                        provider_video_id=video_id,
                        embed_url=f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>',
                        uploader=user
                    )

                    # Update creation date manually
                    video.created_at = published_at
                    
                    video.save(update_fields=['created_at'])

                    videos_imported += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Imported video: {video.title} (Published: {published_at.strftime("%Y-%m-%d")})'
                    ))

                    # Small pause to not exceed API limits
                    time.sleep(1)

            except HttpError as e:
                self.stdout.write(self.style.ERROR(f'YouTube API error: {str(e)}'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {videos_imported} videos')) 