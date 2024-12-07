from rest_framework import generics
from .models import Artist, ArtPiece, Genre, Comment
from .serializers import ArtistSerializer, ArtPieceSerializer, CommentSerializer, GenreSerializer, ProfileSerializer
from .models import Artist, ArtPiece, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import status
import requests
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
import os


def proxy_media(request, path):
    if not settings.MEDIA_URL.startswith(('http://', 'https://')):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if not os.path.exists(file_path):
            raise Http404("Media not found")

        response = FileResponse(open(file_path, 'rb'))
        response['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        media_url = f'{settings.MEDIA_URL}{path}'
        
        try:
            r = requests.get(media_url, stream=True)
            r.raise_for_status()
        except requests.exceptions.RequestException:
            raise Http404("Media not found")
        
        django_response = HttpResponse(
            r.content, 
            content_type=r.headers.get('Content-Type', 'application/octet-stream')
        )
        django_response['Access-Control-Allow-Origin'] = '*'
        return django_response

class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.filter(is_verified=True)
    serializer_class = ArtistSerializer

class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class ArtPieceListCreateView(generics.ListCreateAPIView):
    queryset = ArtPiece.objects.filter(is_verified=True)
    serializer_class = ArtPieceSerializer

class ArtPieceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArtPiece.objects.all()
    serializer_class = ArtPieceSerializer

class ContributedArtistListView(generics.ListAPIView):
    queryset = Artist.objects.filter(is_contributed=True).order_by('-added_time')
    serializer_class = ArtistSerializer

class ContributedArtPieceListView(generics.ListAPIView):
    queryset = ArtPiece.objects.filter(is_contributed=True).order_by('-added_time')
    serializer_class = ArtPieceSerializer

class ContributionsView(APIView):
    def get(self, request):
        # Fetch contributed artists
        artists = [
            {
                "contribution_id": artist.id,
                "type": "Artist",
                "name": artist.name,
                "added_time": artist.added_time,
                "status": artist.status,
            }
            for artist in Artist.objects.filter(is_contributed=True)
        ]

        # Fetch contributed art pieces
        art_pieces = [
            {
                "contribution_id": art_piece.id,
                "type": "ArtPiece",
                "name": art_piece.title,  # Rename 'title' to 'name'
                "added_time": art_piece.added_time,
                "status": art_piece.status,
            }
            for art_piece in ArtPiece.objects.filter(is_contributed=True)
        ]

        # Combine and sort by added_time in descending order
        contributions = sorted(
            artists + art_pieces, key=lambda x: x["added_time"], reverse=True
        )

        return Response(contributions)
    
class GenreListView(generics.ListAPIView):
    """
    API endpoint to list all genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        art_piece_id = self.kwargs['art_piece_id']
        return Comment.objects.filter(art_piece_id=art_piece_id, parent=None)

    def perform_create(self, serializer):
        art_piece_id = self.kwargs['art_piece_id']
        serializer.save(art_piece_id=art_piece_id)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class ProfileDetail(APIView):
    
    def get_object(self, username):
        try:
            return Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return None
    
    def get(self, request, username, format=None):
        profile = self.get_object(username)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, username, format=None):
        profile = self.get_object(username)
        if profile is None:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
