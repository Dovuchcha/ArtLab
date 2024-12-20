# Generated by Django 5.1.3 on 2024-12-01 15:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0010_artpiece_contributor_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artpiece",
            name="artist",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="art_pieces",
                to="gallery.artist",
            ),
        ),
    ]
