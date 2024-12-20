# Generated by Django 5.1.3 on 2024-12-04 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0015_comment"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="artist",
            name="era",
            field=models.CharField(
                choices=[
                    ("Modern", "Modern"),
                    ("Contemporary", "Contemporary"),
                    ("Classical", "Classical"),
                    ("Renaissance", "Renaissance"),
                    ("Baroque", "Baroque"),
                    ("Realism", "Realism"),
                    ("Symbolism", "Symbolism"),
                ],
                default="Modern",
                max_length=50,
            ),
        ),
    ]
