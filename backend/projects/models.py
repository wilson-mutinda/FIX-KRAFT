from django.db import models
from django.utils.text import slugify

# Create your models here.
class Projects(models.Model):

    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('launched', 'Launched'),
        ('maintainance', 'Maintainance'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(max_length=255)
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')

    # Case study fields (optional)
    overview = models.TextField(blank=True, null=True)
    problem = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    tech_stack = models.TextField(blank=True, null=True)
    gallery = models.TextField(blank=True, null=True)
    hero_image = models.ImageField(upload_to='projects/hero/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
