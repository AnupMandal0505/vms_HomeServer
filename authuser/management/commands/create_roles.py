from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create user groups GM, PA, OP"

    def handle(self, *args, **kwargs):
        """Create groups without permissions"""
        group_names = ['GM', 'PA', 'OP','USER','SECRETARY','DISPLAY','CANTEEN']

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group "{group_name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))

        self.stdout.write(self.style.SUCCESS('Groups created successfully!'))
