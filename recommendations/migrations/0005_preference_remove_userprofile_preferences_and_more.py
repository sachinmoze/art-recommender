# Generated by Django 5.0.7 on 2024-08-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0004_alter_gallery_floor_alter_gallery_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='preferences',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferences',
            field=models.ManyToManyField(blank=True, null=True, to='recommendations.preference'),
        ),
    ]
