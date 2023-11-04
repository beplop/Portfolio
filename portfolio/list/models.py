from django.db import models


class Projects(models.Model):
    repo_id = models.IntegerField('ID репозитория', default=0)
    name = models.CharField('Название', max_length=50, default='')
    descript = models.CharField('Описание', max_length=250, default='', null=True)
    date = models.DateField('Дата создания')
    language = models.CharField('Язык программирования', max_length=20, default='', null=True)
    url = models.CharField('Ссылка', max_length=250, default='', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
