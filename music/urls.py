from django.urls import path
from .views import MusicViewSet, FavoritePlaylistViewSet

app_name = 'music'

urlpatterns = [
    # Music URLs
    path('list/', MusicViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='music-list'),
    
    path('<int:pk>/', MusicViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='music-detail'),

    # Favorites URLs
    path('favorites/', FavoritePlaylistViewSet.as_view({
        'get': 'list',
        'post': 'add_music',
        'delete': 'remove_music'
    }), name='favorite-playlist'),
]