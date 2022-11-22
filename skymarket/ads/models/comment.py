from django.conf import settings
from django.db import models
from ads.models.ad import Ad


class Comment(models.Model):
    # TODO добавьте поля модели здесь
    text = models.TextField(max_length=300,
                            default='',
                            null=True,
                            verbose_name="Комментарий",
                            help_text="Оставьте свой комментарий здесь",
                            )
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               default='',
                               related_name='comments',
                               verbose_name="Автор комментария",
                               help_text="Выберите автора комментария",
                               )
    ad = models.ForeignKey(Ad,
                           on_delete=models.CASCADE,
                           default='',
                           related_name="comments",
                           verbose_name="Объявление",
                           help_text="Объявление, к которому относится комментарий",
                           )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Время создания комментария",
                                      help_text="Введите время создания комментария",
                                      )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-created_at",)
