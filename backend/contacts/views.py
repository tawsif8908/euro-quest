from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter
from .models import Contact
from .serializers import (
    ContactSerializer,
    ContactCreateSerializer,
    ContactResponseSerializer,
    ContactStatusUpdateSerializer
)


class ContactFilter(FilterSet):
    status = CharFilter(field_name='status')
    priority = CharFilter(field_name='priority')
    contact_type = CharFilter(field_name='contact_type')

    class Meta:
        model = Contact
        fields = ['status', 'priority', 'contact_type']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContactFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ContactCreateSerializer
        return ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        return Response({
            'success': True,
            'data': ContactSerializer(contact).data,
            'message': 'Message sent successfully'
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def respond(self, request, pk=None):
        """Add response to contact message"""
        contact = self.get_object()
        serializer = ContactResponseSerializer(contact, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': ContactSerializer(contact).data,
                'message': 'Response sent successfully'
            })

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update contact status and priority"""
        contact = self.get_object()
        serializer = ContactStatusUpdateSerializer(contact, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': ContactSerializer(contact).data,
                'message': 'Contact updated successfully'
            })

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)