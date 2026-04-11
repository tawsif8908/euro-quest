from django.db import models
from django.core.validators import MinLengthValidator


class Contact(models.Model):
    CONTACT_TYPES = [
        ('general', 'General Inquiry'),
        ('support', 'Support'),
        ('partnership', 'Partnership'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    email = models.EmailField()
    subject = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    message = models.TextField(max_length=2000, validators=[MinLengthValidator(1)])
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Response tracking
    response_content = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    responded_by = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['email']),
            models.Index(fields=['contact_type']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject}"