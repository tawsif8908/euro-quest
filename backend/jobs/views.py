from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter, ChoiceFilter
from django.db import models
from .models import Job
from .serializers import JobSerializer, JobListSerializer


class JobFilter(FilterSet):
    category = CharFilter(field_name='category', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    search = CharFilter(method='filter_search')

    class Meta:
        model = Job
        fields = ['category', 'location', 'job_type']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(company__icontains=value)
        )


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all unique job categories"""
        categories = Job.objects.filter(
            is_active=True
        ).values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})

    @action(detail=False, methods=['get'])
    def meta(self, request):
        """Get metadata for jobs"""
        categories = Job.objects.filter(
            is_active=True
        ).values_list('category', flat=True).distinct()

        job_types = [{'value': choice[0], 'label': choice[1]} for choice in Job.JOB_TYPES]

        return Response({
            'categories': list(categories),
            'job_types': job_types
        })