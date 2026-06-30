from rest_framework import serializers
from .models import JournalComment


class JournalCommentListSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    author_role = serializers.CharField(
        source="author.role",
        read_only=True,
    )

    class Meta:
        model = JournalComment
        fields = (
            "id",
            "author",
            "author_role",
            "content",
            "created_at",
        )


class JournalCommentDetailSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField()
    author_role = serializers.CharField(
        source="author.role",
        read_only=True,
    )

    class Meta:
        model = JournalComment
        fields = (
            "id",
            "lesson",
            "author",
            "author_role",
            "content",
            "created_at",
            "updated_at",
        )


class JournalCommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = JournalComment
        fields = (
            "content",
        )
