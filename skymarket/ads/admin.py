from django.contrib import admin
from ads.models.ad import Ad
from ads.models.comment import Comment

# TODO здесь можно подключить ваши модели к стандартной джанго-админке
admin.site.register(Ad)
admin.site.register(Comment)
