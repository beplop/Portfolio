# Generated by Django 4.2.6 on 2023-10-22 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0005_alter_projects_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='repo_id',
            field=models.IntegerField(default=0, verbose_name='ID репозитория'),
        ),
    ]