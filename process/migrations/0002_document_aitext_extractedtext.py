# Generated by Django 5.1 on 2024-08-20 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='Documents/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='uploaded', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AIText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.CharField(max_length=255)),
                ('classification', models.CharField(max_length=255)),
                ('sentiment', models.CharField(blank=True, max_length=50, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.document')),
            ],
        ),
        migrations.CreateModel(
            name='ExtractedText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.document')),
            ],
        ),
    ]
