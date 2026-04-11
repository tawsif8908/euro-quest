from rest_framework import serializers
from .models import Application
from jobs.serializers import JobListSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    job_details = JobListSerializer(source='job', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_details', 'applicant_name', 'email', 'phone',
            'resume', 'cover_letter', 'experience_level', 'skills',
            'availability', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Check if user already applied for this job
        job = data.get('job')
        email = data.get('email')

        if job and email:
            existing = Application.objects.filter(job=job, email=email)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("You have already applied for this job")

        return data


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating applications"""

    class Meta:
        model = Application
        fields = [
            'job', 'applicant_name', 'email', 'phone', 'resume',
            'cover_letter', 'experience_level', 'skills', 'availability'
        ]

    def validate_job(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This job is no longer accepting applications")
        return value


class ApplicationStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Application.STATUS_CHOICES)

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance