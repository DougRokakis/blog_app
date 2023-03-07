# Generated by Django 4.1.6 on 2023-03-07 14:53

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theblog', '0011_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_code', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Code')),
            ],
        ),
    ]