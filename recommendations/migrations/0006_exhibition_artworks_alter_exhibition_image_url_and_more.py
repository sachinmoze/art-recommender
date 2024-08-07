# Generated by Django 5.0.7 on 2024-08-05 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0005_preference_remove_userprofile_preferences_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibition',
            name='artworks',
            field=models.ManyToManyField(related_name='exhibitions', to='recommendations.artwork'),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='image_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='short_description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='exhibition',
            name='web_url',
            field=models.URLField(max_length=255),
        ),
    ]
