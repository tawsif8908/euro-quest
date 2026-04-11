from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from jobs.models import Job


class Application(models.Model):
    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive Level'),
    ]

    AVAILABILITY_CHOICES = [
        ('immediately', 'Immediately'),
        ('2-weeks', '2 Weeks'),
        ('1-month', '1 Month'),
        ('3-months', '3 Months'),
        ('negotiable', 'Negotiable'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?[\d\s\-\(\)]+$',
            message='Enter a valid phone number'
        )]
    )
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(max_length=2000, blank=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS)
    skills = models.JSONField(default=list, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='negotiable')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"

    def save(self, *args, **kwargs):
        # Update job's application count when status changes
        if self.pk:  # Only for existing applications
            old_status = Application.objects.get(pk=self.pk).status
            if old_status != self.status:
                # Could add logic here to update job statistics
                pass
        super().save(*args, **kwargs)