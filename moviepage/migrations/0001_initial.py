# Generated by Django 5.1.5 on 2025-02-03 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=4, null=True)),
                ('rated', models.CharField(blank=True, max_length=10, null=True)),
                ('released', models.CharField(blank=True, max_length=20, null=True)),
                ('runtime', models.CharField(blank=True, max_length=20, null=True)),
                ('genre', models.CharField(blank=True, max_length=255, null=True)),
                ('director', models.CharField(blank=True, max_length=255, null=True)),
                ('writer', models.CharField(blank=True, max_length=255, null=True)),
                ('actors', models.TextField(blank=True, null=True)),
                ('plot', models.TextField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('awards', models.TextField(blank=True, null=True)),
                ('poster', models.URLField(blank=True, null=True)),
                ('imdb_rating', models.CharField(blank=True, max_length=5, null=True)),
                ('imdb_id', models.CharField(max_length=20, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('available', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], default='active', max_length=50)),
            ],
        ),
    ]
