from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    salary = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'job_type', 'category',
            'description', 'requirements', 'salary', 'benefits',
            'application_deadline', 'contact_email', 'is_active',
            'featured', 'views', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'views', 'created_at', 'updated_at']

    def get_salary(self, obj):
        if obj.salary_min or obj.salary_max:
            salary_info = {
                'currency': obj.salary_currency,
                'period': obj.salary_period,
            }
            if obj.salary_min:
                salary_info['min'] = float(obj.salary_min)
            if obj.salary_max:
                salary_info['max'] = float(obj.salary_max)
            return salary_info
        return None

    def validate(self, data):
        # Custom validation for salary range
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError("Minimum salary cannot be greater than maximum salary")

        return data


class JobListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    salary = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'job_type', 'category',
            'salary', 'application_deadline', 'is_active', 'featured', 'created_at'
        ]

    def get_salary(self, obj):
        if obj.salary_min or obj.salary_max:
            return {
                'currency': obj.salary_currency,
                'period': obj.salary_period,
                'min': float(obj.salary_min) if obj.salary_min else None,
                'max': float(obj.salary_max) if obj.salary_max else None,
            }
        return None