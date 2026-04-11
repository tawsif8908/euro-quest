from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify


class Blog(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(max_length=300, validators=[MinLengthValidator(1)])
    content = models.TextField(validators=[MinLengthValidator(1)])

    # Author information
    author_name = models.CharField(max_length=100, blank=True)
    author_email = models.EmailField(blank=True)
    author_bio = models.TextField(blank=True)

    category = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    tags = models.JSONField(default=list, blank=True)

    # Media
    featured_image_url = models.URLField(blank=True)
    featured_image_alt = models.CharField(max_length=200, blank=True)

    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)

    # Statistics
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def increment_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.title}"