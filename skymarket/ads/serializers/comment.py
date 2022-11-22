from rest_framework import serializers
from ads.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')
    author_id = serializers.ReadOnlyField(source='author.id')
    author_first_name = serializers.CharField(source='author.first_name')
    ad_id = serializers.IntegerField(source='ad.id')

    class Meta:
        model = Comment
        exclude = ["id", "ad", "author"]


class CommentCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author_id = serializers.ReadOnlyField(source='author.id')
    author_first_name = serializers.ReadOnlyField(source='author.first_name')
    author_last_name = serializers.ReadOnlyField(source='author.last_name')
    ad_id = serializers.ReadOnlyField(source='ad.id')

    pk = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Comment
        exclude = ['author']
