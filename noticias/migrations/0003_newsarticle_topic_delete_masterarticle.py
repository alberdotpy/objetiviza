# Generated by Django 4.2.4 on 2024-10-26 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0002_masterarticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='topic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='MasterArticle',
        ),
    ]
