from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Music(models.Model):
    CATEGORY_CHOICES = [
        ('sleep', 'Sleep'),
        ('focus', 'Focus'),
        ('emotional_healing', 'Emotional Healing'),
        ('nature', 'Nature'),
        ('instrumental', 'Instrumental'),
    ]
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True, null=True)
    music_file = models.FileField(upload_to='music/')
    banner = models.ImageField(upload_to='music_banners/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='instrumental')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FavoritePlaylist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite_playlist')
    music = models.ManyToManyField(Music, related_name='favorited_by', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Favorite Playlist"