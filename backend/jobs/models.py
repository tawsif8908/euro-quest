from django.db import models
from django.core.validators import MinLengthValidator


class Job(models.Model):
    JOB_TYPES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    company = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    location = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full-time')
    category = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    description = models.TextField(validators=[MinLengthValidator(1)])
    requirements = models.JSONField(default=list, blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='EUR')
    salary_period = models.CharField(max_length=10, choices=[
        ('hour', 'per hour'),
        ('day', 'per day'),
        ('week', 'per week'),
        ('month', 'per month'),
        ('year', 'per year'),
    ], default='year')
    benefits = models.JSONField(default=list, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        indexes = [
            models.Index(fields=['category', 'location', 'job_type']),
            models.Index(fields=['is_active', 'featured']),
        ]

    def __str__(self):
        return f"{self.title} at {self.company}"

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])