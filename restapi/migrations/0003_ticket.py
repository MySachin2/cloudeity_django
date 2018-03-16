# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-14 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_category_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.FileField(upload_to=b'images/')),
                ('ticket_name', models.CharField(max_length=100)),
                ('type_of_feedback', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
