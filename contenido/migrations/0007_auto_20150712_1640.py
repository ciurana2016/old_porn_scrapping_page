# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0006_auto_20150711_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paginatube',
            name='altura',
        ),
        migrations.RemoveField(
            model_name='paginatube',
            name='anchura',
        ),
    ]
