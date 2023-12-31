# Generated by Django 4.2.6 on 2023-10-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.RenameField(
            model_name='projects',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='anons',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='full_text',
        ),
        migrations.AddField(
            model_name='projects',
            name='descript',
            field=models.CharField(default='', max_length=250, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='projects',
            name='language',
            field=models.CharField(default='', max_length=20, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='date',
            field=models.DateTimeField(verbose_name='Дата создания'),
        ),
    ]
