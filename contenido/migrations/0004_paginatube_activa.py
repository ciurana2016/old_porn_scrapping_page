# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0003_video_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='paginatube',
            name='activa',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
