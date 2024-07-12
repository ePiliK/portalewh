from django.core.management.base import BaseCommand
from linkmanager.models import Client

class Command(BaseCommand):
    help = 'Import clients from a text file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the text file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as file:
            for line in file:
                name = line.strip()
                Client.objects.create(name=name)
                self.stdout.write(self.style.SUCCESS(f'Successfully created client "{name}"'))