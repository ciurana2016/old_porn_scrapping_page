# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='pagina_tube',
            field=models.ForeignKey(blank=True, to='contenido.PaginaTube', null=True),
        ),
    ]
