from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'subject', 'message', 'contact_type',
            'status', 'priority', 'response_content', 'responded_at',
            'responded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating contact messages"""

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message', 'contact_type']


class ContactResponseSerializer(serializers.Serializer):
    response_content = serializers.CharField()
    responded_by = serializers.CharField()

    def update(self, instance, validated_data):
        instance.response_content = validated_data['response_content']
        instance.responded_by = validated_data['responded_by']
        instance.status = 'responded'
        from django.utils import timezone
        instance.responded_at = timezone.now()
        instance.save()
        return instance


class ContactStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Contact.STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=Contact.PRIORITY_CHOICES, required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance