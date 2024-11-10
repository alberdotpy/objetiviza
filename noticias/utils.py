from noticias.sandbox.newspapers import newspapers
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'objetiviza.settings')
django.setup()
from noticias.models import Periodico

def importar_periodicos():
    for url, details in newspapers.items():
        Periodico.objects.get_or_create(
            url=url,
            defaults={
                'title': details['title'],
                'alignment': details['alignment'],
                'replace_words': details['replace_words'],
                'logo_url': details.get('logo_url', None),  # Usa el logo_url si está disponible
            }
        )
    print('Periódicos importados con éxito.')

# Llama a la función para importar periódicos
importar_periodicos()