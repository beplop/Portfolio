from django.db import models


class Projects(models.Model):
    name = models.CharField('Название', max_length=50, default='')
    descript = models.CharField('Описание', max_length=250, default='', null=True)
    date = models.DateTimeField('Дата создания')
    language = models.CharField('Язык программирования', max_length=20, default='', null=True)

    # title = models.CharField('Название', max_length=50, default='')
    # anons = models.CharField('Анонс', max_length=250, default='')
    # full_text = models.TextField('Статья')
    # date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
