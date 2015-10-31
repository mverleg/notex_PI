# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64, validators=[django.core.validators.RegexValidator('[a-zA-Z][a-zA-Z0-9_.]*', 'Package names may contain only letters, numbers, periods and underscores and must start with a letter.')], db_index=True, unique=True)),
                ('license_name', models.CharField(max_length=32)),
                ('readme_name', models.CharField(max_length=32, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_\\-.]{1,32}$', 'File and directory names may have a length up to 32 selected from alphanumeric characters, periods, dashes and underscores.')], blank=True)),
                ('listed', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Package',
            },
        ),
        migrations.CreateModel(
            name='PackageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('version', models.PositiveIntegerField(help_text='10000 * major + minor')),
                ('rest', models.CharField(max_length=24, validators=[django.core.validators.RegexValidator('^[^.][a-zA-Z0-9_\\-.]+$', 'Versions may contain only letters, numbers, periods, dashes and underscores.')], blank=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('listed', models.BooleanField(default=True)),
                ('package', models.ForeignKey(to='pindex.PackageSeries', related_name='versions')),
            ],
            options={
                'verbose_name': 'Version',
                'ordering': ('-when',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='packageversion',
            unique_together=set([('package', 'version', 'rest')]),
        ),
    ]
