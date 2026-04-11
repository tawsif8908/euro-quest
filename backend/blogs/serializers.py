from rest_framework import serializers
from .models import Blog, BlogComment


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['id', 'name', 'email', 'content', 'approved', 'created_at']
        read_only_fields = ['id', 'created_at']


class BlogSerializer(serializers.ModelSerializer):
    comments = BlogCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'author_name',
            'author_email', 'author_bio', 'category', 'tags',
            'featured_image_url', 'featured_image_alt', 'status',
            'published_at', 'views', 'likes', 'comments', 'comments_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'views', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.comments.filter(approved=True).count()


class BlogListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author_name', 'category',
            'featured_image_url', 'featured_image_alt', 'status',
            'published_at', 'views', 'likes', 'comments_count', 'created_at'
        ]

    def get_comments_count(self, obj):
        return obj.comments.filter(approved=True).count()


class BlogCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating blog posts"""

    class Meta:
        model = Blog
        fields = [
            'title', 'excerpt', 'content', 'author_name', 'author_email',
            'author_bio', 'category', 'tags', 'featured_image_url',
            'featured_image_alt', 'status'
        ]


class BlogCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating blog comments"""

    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'content']