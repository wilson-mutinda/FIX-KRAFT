from django.core.management.base import BaseCommand
from mediahub.models import MediaCategory

class Command(BaseCommand):

    help = 'Seed default media categories'

    def handle(self, *args, **kwargs):

        categories = [
            {
                "name": "Logos",
                "description": "Brand identity and logo designs"
            },

            {
                "name": "Social Media",
                "description": "Social media creatives and campaigns"
            },

            {
                "name": "Flyers",
                "description": "Marketing flyers and promotions"
            },

            {
                "name": "Posters",
                "description": "Poster and campaign designs"
            },

            {
                "name": "Mockups",
                "description": "Product and branding mockups"
            },

            {
                "name": "UI/UX",
                "description": "User interface and experience designs"
            },

            {
                "name": "Web Design",
                "description": "Website layouts and concepts"
            },

            {
                "name": "CMS Projects",
                "description": "Content management system projects"
            },

            {
                "name": "Brand Identity",
                "description": "Complete branding systems"
            },

            {
                "name": "Business Cards",
                "description": "Professional business card designs"
            },

            {
                "name": "Bronchures",
                "description": "Corporate bronchures and booklets"
            },

            {
                "name": "Banners",
                "description": "Digital and print banners"
            },

            {
                "name": "Motion Graphics",
                "description": "Animations and motion design"
            },

            {
                "name": "Photography",
                "description": "Photography and editing"
            },

            {
                "name": "Printing",
                "description": "Printing and merchandise work"
            }
        ]

        for category in categories:

            obj, created = MediaCategory.objects.get_or_create(
                name = category['name'],
                defaults={
                    'description': category['description']
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {obj.name}"
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Already exists: {obj.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Seeding completed successfully."
            )
        )
