from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Music, FavoritePlaylist
from .serializers import MusicSerializer, FavoritePlaylistSerializer
from .permissions import IsAdminOrReadOnly, IsSubscribed, IsOwnerOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

@extend_schema_view(
    list=extend_schema(
        summary="List all music tracks",
        description="Retrieve a list of all available music tracks. Access requires subscription.",
        tags=["Music"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific music track",
        description="Retrieve details of a single music track by its ID. Access requires subscription.",
        tags=["Music"]
    ),
    create=extend_schema(
        summary="Upload a new music track",
        description="Upload a new music track. Only accessible by admin users.",
        tags=["Music"]
    ),
    update=extend_schema(
        summary="Update an existing music track",
        description="Update all fields of an existing music track by its ID. Only accessible by admin users.",
        tags=["Music"]
    ),
    partial_update=extend_schema(
        summary="Partially update an existing music track",
        description="Update some fields of an existing music track by its ID. Only accessible by admin users.",
        tags=["Music"]
    ),
    destroy=extend_schema(
        summary="Delete a music track",
        description="Delete a music track by its ID. Only accessible by admin users.",
        tags=["Music"]
    )
)
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsSubscribed]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

@extend_schema_view(
    list=extend_schema(
        summary="Get user's favorite playlist",
        description="Retrieve the favorite playlist for the authenticated user.",
        tags=["Favorite Playlist"]
    ),
    add_music=extend_schema(
        summary="Add music to favorite playlist",
        description="Add a music track to the authenticated user's favorite playlist.",
        tags=["Favorite Playlist"]
    ),
    remove_music=extend_schema(
        summary="Remove music from favorite playlist",
        description="Remove a music track from the authenticated user's favorite playlist.",
        tags=["Favorite Playlist"]
    )
)
class FavoritePlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritePlaylistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return FavoritePlaylist.objects.filter(user=self.request.user).prefetch_related('music')

    def get_object(self):
        playlist, created = FavoritePlaylist.objects.get_or_create(user=self.request.user)
        return playlist

    def list(self, request, *args, **kwargs):
        # Ensure the favorite playlist exists for the user
        FavoritePlaylist.objects.get_or_create(user=self.request.user)
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_music(self, request, pk=None):
        playlist = self.get_object()
        music = Music.objects.get(pk=request.data.get('music_id'))
        playlist.music.add(music)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_music(self, request, pk=None):
        playlist = self.get_object()
        music = Music.objects.get(pk=request.data.get('music_id'))
        playlist.music.remove(music)
        return Response(status=status.HTTP_200_OK)