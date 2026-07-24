from rest_framework import serializers
from .models import Music, FavoritePlaylist

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

class FavoritePlaylistSerializer(serializers.ModelSerializer):
    music = MusicSerializer(many=True, read_only=True)
    music_ids = serializers.PrimaryKeyRelatedField(queryset=Music.objects.all(), many=True, write_only=True, source='music')

    class Meta:
        model = FavoritePlaylist
        fields = ['id', 'music', 'music_ids', 'created_at', 'updated_at']
        read_only_fields = ('user',)