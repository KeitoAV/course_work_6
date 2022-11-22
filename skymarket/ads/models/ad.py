from django.conf import settings
from django.db import models


class Ad(models.Model):
    # TODO добавьте поля модели здесь
    title = models.CharField(max_length=60,
                             verbose_name="Название товара",
                             help_text="введите название товара",
                             )
    price = models.PositiveIntegerField(default=0,
                                        verbose_name="Цена товара",
                                        help_text="Добавьте цену товара"
                                        )
    description = models.TextField(max_length=300,
                                   default='',
                                   null=True,
                                   verbose_name="Описание товара",
                                   help_text="Введите описание товара"
                                   )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               default='',
                               related_name='ads',
                               verbose_name="Автор объявления",
                               help_text="Выберите автора объявления",
                               )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания объявления",
                                      help_text="Введите время создания объявления",
                                      )
    image = models.ImageField(upload_to='images/',
                              null=True,
                              verbose_name="фото",
                              help_text="Разместите фото для объявления"
                              )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']
