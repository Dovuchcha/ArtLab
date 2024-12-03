from django.db import models
from django.utils.timezone import now

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Artist(models.Model):
    ERA_CHOICES = [
        ('Modern', 'Modern'),
        ('Contemporary', 'Contemporary'),
        ('Classical', 'Classical'),
        ('Renaissance', 'Renaissance'),
        ('Baroque', 'Baroque'),
        ('Realism', 'Realism'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)  # Optional death date for deceased artists
    profile_picture = models.ImageField(upload_to='artists/', null=True, blank=True)
    era = models.CharField(max_length=50, choices=ERA_CHOICES, default='Modern')
    is_verified = models.BooleanField(default=False)
    contributor_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')  # Status field
    added_time = models.DateTimeField(default=now)
    is_contributed = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_deceased(self):
        """Returns True if the artist has a death_date, otherwise False."""
        return self.death_date is not None

class ArtPiece(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='art_pieces', default=1)
    image = models.ImageField(upload_to='art_pieces/', null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='art_pieces', null=True, blank=True)
    medium = models.CharField(max_length=100, null=True, blank=True)
    style = models.CharField(max_length=100, null=True, blank=True)
    created_year = models.IntegerField()
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    contributor_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')  # Status field
    added_time = models.DateTimeField(default=now)
    is_contributed = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    

class Comment(models.Model):
    art_piece = models.ForeignKey(
        ArtPiece,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f'Comment by Anonymous on {self.art_piece.title} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']