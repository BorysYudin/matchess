# Generated by Django 2.2.1 on 2019-05-19 21:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('is_started', models.BooleanField(default=False)),
                ('is_expired', models.BooleanField(default=False)),
                ('black_pieces_player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='black_pieces_player', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('white_pieces_player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='white_pieces_player', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]