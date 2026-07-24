from django.contrib import admin
from .models import Music, FavoritePlaylist

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'artist')

@admin.register(FavoritePlaylist)
class FavoritePlaylistAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    filter_horizontal = ('music',)