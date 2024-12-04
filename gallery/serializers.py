from rest_framework import serializers
from .models import Artist, ArtPiece, Genre, Comment, Profile

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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']
    
    def validate_username(self, value):
        """
        Ensure that the username is alphanumeric and between 3 to 150 characters.
        """
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric.")
        if not (3 <= len(value) <= 150):
            raise serializers.ValidationError("Username must be between 3 and 150 characters long.")
        return value
    
    def validate_email(self, value):
        """
        Ensure that the email has a valid format and is unique.
        """
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'art_piece', 'parent', 'content', 'timestamp', 'replies', 'owner']
        read_only_fields = ['id', 'timestamp', 'replies']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Include detailed owner information
        owner = instance.owner
        representation['owner'] = {
            'id': owner.id,
            'username': owner.username,
            'email': owner.email
        }

        return representation