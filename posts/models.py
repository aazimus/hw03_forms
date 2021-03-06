from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        verbose_name = 'Название группы',
        max_length=200,
        help_text='Дайте название вашей группе'
    )
    slug = models.SlugField(
        verbose_name = 'Адрес для страницы с группой',
        unique=True,
        max_length=100,
        blank=True,
        help_text=('Укажите адрес для страницы задачи. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )
    description = models.TextField(
        verbose_name = 'Описание группы',
        help_text = 'Дайте описание группы'
        )

    def __str__(self):
        return self.title


class Post(models.Model):

    text = models.TextField(
        verbose_name = 'Текст вашего поста',
        help_text='Содержание вашего поста'
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name = 'Автор',
        help_text = 'Автор поста',
        on_delete=models.CASCADE,
        related_name="posts")
    group = models.ForeignKey(               
        Group,
        verbose_name = 'Группа',
        help_text = 'Сожержание группы' ,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts")

    def __str__(self):
        return (
            #f'AUTHOR: {self.author.username} '
            #f'GROUP: {self.group} '
            #f'DATE: {self.pub_date.strftime("%d-%m-%Y-%H.%M.%S")} '
            #f'TEXT: {self.text[0:15]}'
            self.text[0:15]
        )

    class Meta:
        ordering = ("-pub_date",)
