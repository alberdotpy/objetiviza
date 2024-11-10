from django.core.management.base import BaseCommand
from models import Periodico
from newspapers import newspapers

class Command(BaseCommand):
    help = 'Importa periódicos a la base de datos'

    def handle(self, *args, **kwargs):
        for url, details in newspapers.items():
            Periodico.objects.get_or_create(
                url=url,
                defaults={
                    'title': details['title'],
                    'alignment': details['alignment'],
                    'replace_words': details['replace_words'],
                    'logo_url': None,  # Puedes poner un valor por defecto o None
                }
            )
        self.stdout.write(self.style.SUCCESS('Periódicos importados con éxito.'))
