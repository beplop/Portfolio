# Generated by Django 4.2.6 on 2023-10-22 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0003_alter_projects_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='descript',
            field=models.CharField(default='', max_length=250, null=True, verbose_name='Описание'),
        ),
    ]
