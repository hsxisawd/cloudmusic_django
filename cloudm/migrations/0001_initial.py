# Generated by Django 2.2.12 on 2022-04-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playlists',
            fields=[
                ('id', models.CharField(default='', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True)),
                ('tags', models.CharField(max_length=255, null=True)),
                ('create_time', models.CharField(max_length=255, null=True)),
                ('update_time', models.CharField(max_length=255, null=True)),
                ('tracks_num', models.IntegerField(null=True)),
                ('play_count', models.IntegerField(null=True)),
                ('subscribed_count', models.IntegerField(null=True)),
                ('share_count', models.IntegerField(null=True)),
                ('comment_count', models.IntegerField(null=True)),
                ('nickname', models.CharField(max_length=255, null=True)),
                ('gender', models.CharField(max_length=255, null=True)),
                ('user_type', models.CharField(max_length=255, null=True)),
                ('vip_type', models.CharField(max_length=255, null=True)),
                ('province', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'playlists',
            },
        ),
    ]