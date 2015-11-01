# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageSeries',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('[a-z][a-z0-9_]{0,31}', 'Package names may contain up to 32 lowercase letters, numbers and underscores and must start with a letter.')], db_index=True, unique=True)),
                ('license_name', models.CharField(max_length=32)),
                ('readme_name', models.CharField(max_length=32, blank=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_\\-.]{1,32}$', 'File and directory names may contain up to 32 alphanumeric characters, periods, dashes and underscores.')])),
                ('listed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='packages')),
            ],
            options={
                'verbose_name': 'Package',
            },
        ),
        migrations.CreateModel(
            name='PackageVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('version', models.PositiveIntegerField(help_text='10000 * major + minor')),
                ('rest', models.CharField(max_length=24, blank=True, validators=[django.core.validators.RegexValidator('^[^.][a-zA-Z0-9_\\-.]+$', 'Version numbers should be formatted like 1.0.dev7, the first two being under 46338')])),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('listed', models.BooleanField(default=True)),
                ('package', models.ForeignKey(to='indx.PackageSeries', related_name='versions')),
            ],
            options={
                'verbose_name': 'Version',
                'ordering': ('-version',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='packageversion',
            unique_together=set([('package', 'version', 'rest')]),
        ),
    ]
