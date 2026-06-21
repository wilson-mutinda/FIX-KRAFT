from django.db import models

# Create your models here.
class Projects(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True
    )

    technologies = models.CharField(
        max_length=255
    )

    project_url = models.URLField(
        blank=True,
        null=True
    )

    github_url = models.URLField(
        blank=True,
        null=True
    )

    featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
