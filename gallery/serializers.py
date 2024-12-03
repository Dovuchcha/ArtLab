from rest_framework import serializers
from .models import Artist, ArtPiece, Genre, Comment

class ArtistSerializer(serializers.ModelSerializer):
    is_deceased = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = '__all__'

    def get_is_deceased(self, obj):
        """Returns True if the artist has a death_date, otherwise False."""
        return obj.is_deceased()

class ArtPieceSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())

    class Meta:
        model = ArtPiece
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.image and request:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'art_piece', 'parent', 'content', 'timestamp', 'replies']
        read_only_fields = ['id', 'timestamp', 'replies']