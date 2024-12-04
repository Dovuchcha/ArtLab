from django.contrib import admin
from .models import Artist, ArtPiece, Genre, Comment, Profile

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'era', 'birth_date', 'status', 'is_deceased')
    list_filter = ('era', 'birth_date', 'death_date', 'status')
    search_fields = ('name', 'era')

@admin.register(ArtPiece)
class ArtPieceAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_year', 'get_genres')  # Use custom method for genres
    list_filter = ('created_year', 'medium', 'style', 'genres', 'status')  # Use 'genres' directly for filtering
    search_fields = ('title', 'artist__name')
    filter_horizontal = ('genres',)  # For Many-to-Many fields

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()]) 
    get_genres.short_description = 'Genres' 

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Comment)
admin.site.register(Profile)