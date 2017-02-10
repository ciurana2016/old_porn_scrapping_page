# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0005_auto_20150711_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modelo',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='paginapago',
            name='imagen',
        ),
        migrations.AddField(
            model_name='modelo',
            name='thumbnail',
            field=models.CharField(default=b'static/imagenes/nothumb.png', max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='paginapago',
            name='thumbnail',
            field=models.CharField(default=b'static/imagenes/nothumb.png', max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='thumbnail',
            field=models.CharField(default=b'static/imagenes/nothumb.png', max_length=120),
            preserve_default=True,
        ),
    ]
