from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
    ApplicationStatusUpdateSerializer
)


class ApplicationFilter(FilterSet):
    job = CharFilter(field_name='job__id')
    status = CharFilter(field_name='status')
    email = CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = Application
        fields = ['job', 'status', 'experience_level']


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related('job')
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update application status"""
        application = self.get_object()
        serializer = ApplicationStatusUpdateSerializer(
            application,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': ApplicationSerializer(application).data,
                'message': 'Application status updated successfully'
            })

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_job(self, request):
        """Get applications for a specific job"""
        job_id = request.query_params.get('job_id')
        if not job_id:
            return Response({
                'success': False,
                'message': 'job_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        applications = self.get_queryset().filter(job_id=job_id)
        serializer = self.get_serializer(applications, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })