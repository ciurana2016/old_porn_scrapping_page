# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0004_paginatube_activa'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo',
            name='numero_videos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paginapago',
            name='numero_videos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='numero_videos',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
