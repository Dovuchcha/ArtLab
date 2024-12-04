from django.urls import path, include
from .views import (
    ArtistListCreateView,
    ArtistRetrieveUpdateDestroyView,
    ArtPieceListCreateView,
    ArtPieceRetrieveUpdateDestroyView,
    ContributedArtistListView,
    ContributedArtPieceListView,
    ContributionsView,
    GenreListView,
    GenreRetrieveUpdateDestroyView,
    CommentListCreateView,
    ProfileDetail,
    ProfileViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('artists/', ArtistListCreateView.as_view(), name='artist_list'),
    path('artists/<int:pk>/', ArtistRetrieveUpdateDestroyView.as_view(), name='artist_detail'),
    path('art_pieces/', ArtPieceListCreateView.as_view(), name='art_piece_list'),
    path('art_pieces/<int:pk>/', ArtPieceRetrieveUpdateDestroyView.as_view(), name='art_piece_detail'),
    path('contributed/artists/', ContributedArtistListView.as_view(), name='contributed_artist_list'),
    path('contributed/art_pieces/', ContributedArtPieceListView.as_view(), name='contributed_art_piece_list'),
    path('contributions/', ContributionsView.as_view(), name='contributions'),
    path('genres/', GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', GenreRetrieveUpdateDestroyView.as_view(), name='genre_detail'),
    path(
        'art_pieces/<int:art_piece_id>/comments/',
        CommentListCreateView.as_view(),
        name='comment-list-create'
    ),
    path('api/profiles/<str:username>/', ProfileDetail.as_view(), name='profile-detail'),
    path('', include(router.urls)),
]