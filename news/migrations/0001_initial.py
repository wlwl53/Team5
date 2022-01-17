# Generated by Django 3.2.10 on 2022-01-10 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('newsno', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('ymd', models.CharField(max_length=10)),
                ('rdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
