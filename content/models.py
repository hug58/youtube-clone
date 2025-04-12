from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.db.models import Count, Q, F
from datetime import timedelta


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.content_object}'


class Video(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    embed_url = models.TextField()
    provider_video_id = models.CharField(max_length=20, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_videos', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_videos', blank=True)
    comments = GenericRelation('Comment')
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_likes_count(self):
        return self.likes.count()

    def get_dislikes_count(self):
        return self.dislikes.count()

    def get_total_reactions(self):
        return self.get_likes_count() + self.get_dislikes_count()

    def get_likes_percentage(self):
        total = self.get_total_reactions()
        if total == 0:
            return 0
        return (self.get_likes_count() / total) * 100

    def calculate_popularity(self):
        # Calculate base score
        score = 0
        score += self.likes.count() * 10  # +10 points per like
        score -= self.dislikes.count() * 5  # -5 points per dislike
        score += self.comments.count()  # +1 point per comment


        days_difference = (timezone.now().date() - self.created_at.date()).days

        """
        The videos of today have 100 more popularity points than the videos of yesterday and so on.
        This means that old videos have a penalty of popularity points for each day, since the new ones
        will have 100 more points than yesterday.
        """

        score -= days_difference * 100

        self.popularity = score
        self.save(update_fields=['popularity'])
        return score

    @classmethod
    def get_top_videos_this_month(cls, limit=5):
        # Get the start date of the current month
        start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get the most popular videos of the current month
        return cls.objects.filter(
            created_at__gte=start_of_month
        ).order_by('-popularity')[:limit]

    @classmethod
    def update_all_popularity(cls):
        # Update popularity for all videos
        for video in cls.objects.all():
            video.calculate_popularity()

    @property
    def likes_count_display(self):
        return f"{self.get_likes_count()} likes"

    @property
    def dislikes_count_display(self):
        return f"{self.get_dislikes_count()} dislikes"

