from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from django.shortcuts import get_object_or_404
from .models import Blog, BlogComment
from .serializers import (
    BlogSerializer,
    BlogListSerializer,
    BlogCreateSerializer,
    BlogCommentSerializer,
    BlogCommentCreateSerializer
)


class BlogFilter(FilterSet):
    category = CharFilter(field_name='category', lookup_expr='icontains')
    status = CharFilter(field_name='status')
    author = CharFilter(field_name='author_name', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ['category', 'status']


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilter

    def get_queryset(self):
        if self.action == 'list':
            # Only show published posts in list view
            return Blog.objects.filter(status='published').prefetch_related('comments')
        return Blog.objects.all().prefetch_related('comments')

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        elif self.action == 'create':
            return BlogCreateSerializer
        return BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        # Allow retrieval by slug for published posts
        lookup_value = kwargs.get('pk')
        if not lookup_value.isdigit():
            # It's a slug
            blog = get_object_or_404(Blog, slug=lookup_value, status='published')
        else:
            blog = self.get_object()

        blog.increment_views()
        serializer = self.get_serializer(blog)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Increment likes for a blog post"""
        blog = self.get_object()
        blog.increment_likes()
        return Response({
            'success': True,
            'likes': blog.likes,
            'message': 'Blog post liked'
        })

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a blog post"""
        blog = self.get_object()
        serializer = BlogCommentCreateSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(blog=blog)
            return Response({
                'success': True,
                'data': BlogCommentSerializer(comment).data,
                'message': 'Comment added successfully'
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique blog categories"""
        categories = Blog.objects.filter(
            status='published'
        ).values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})

    @action(detail=False, methods=['get'])
    def meta(self, request):
        """Get metadata for blogs"""
        categories = Blog.objects.filter(
            status='published'
        ).values_list('category', flat=True).distinct()

        return Response({
            'categories': list(categories)
        })