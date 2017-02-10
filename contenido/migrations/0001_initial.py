# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('nombre_api', models.CharField(max_length=40, blank=True)),
                ('numero_videos', models.IntegerField(default=0)),
                ('thumbnail', models.CharField(default=b'static/imagenes/nothumb.png', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PaginaPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('nombre_api', models.CharField(max_length=40, blank=True)),
                ('numero_videos', models.IntegerField(default=0)),
                ('thumbnail', models.CharField(default=b'static/imagenes/nothumb.png', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='PaginaTube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('imagen', models.ImageField(default=b'static/noimg.png', upload_to=b'static/paginatube/')),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('nombre_api', models.CharField(max_length=20, blank=True)),
                ('numero_videos', models.IntegerField(default=0)),
                ('thumbnail', models.CharField(default=b'static/imagenes/nothumb.png', max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo_iframe', models.CharField(max_length=300, null=True, blank=True)),
                ('publicado', models.DateTimeField(null=True)),
                ('titulo', models.CharField(max_length=70)),
                ('thumbnail', models.CharField(default=b'static/imagenes/nothumb.png', max_length=120)),
                ('url_video', models.CharField(max_length=300, null=True, blank=True)),
                ('slug', models.SlugField(default=b'', max_length=70, editable=False, blank=True)),
                ('casting', models.ManyToManyField(to='contenido.Modelo', null=True)),
                ('pagina_pago', models.ManyToManyField(to='contenido.PaginaPago', null=True)),
                ('pagina_tube', models.ForeignKey(blank=True, to='contenido.PaginaTube', null=True)),
                ('tags', models.ManyToManyField(to='contenido.Tag', null=True)),
            ],
        ),
    ]
