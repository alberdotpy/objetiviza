from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from gnews import GNews
from newspapers import newspapers
import django
import os
from collections import Counter
import re
from email.utils import parsedate_to_datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'objetiviza.settings')
django.setup()

from noticias.models import NewsArticle, Periodico

# Inicializar GNews
#google_news = GNews(language='es', country='ES', period='1d', max_results=100)
google_news = GNews(language='es', country='ES', start_date=(2024, 10, 25), end_date=(2024, 10, 28), max_results=200)

# Listas para almacenar datos de artículos
descripciones = []
articulos_info = []
exclude_keywords = ['noticias', 'programación tv', 'horóscopo', 'guía de tv', 'sudoku', 'crucigrama', 'directo', 'en imágenes',
                    'el tiempo', 'meteo', 'esquelas', 'última hora', 'resumen, goles', 'horario y', 'bonoloto', 'sorteo']
min_words_in_title = 7
min_sample = 4
eps = 0.22

# Obtener artículos por sitio de noticias
for newspaper_url, nombre_periodico in newspapers.items():
    articles = google_news.get_news_by_site(newspaper_url)
    print(nombre_periodico, 'articulos : ', str(len(articles)))
    for article in articles:

        if any(keyword.lower() in article['title'].lower() or keyword.lower() in article['description'].lower() for
               keyword in exclude_keywords):
            continue

        # Reemplazar palabras en el título y la descripción
        replace_words = nombre_periodico['replace_words']
        title_replaced = article['title'].replace(replace_words, '').strip()

        title_word_count = len(title_replaced.split())
        if title_word_count < min_words_in_title:
            continue

        description_replaced = article['description'].replace(replace_words, '').strip() if article[
            'description'] else ''
        descripciones.append(title_replaced)
        published_date = parsedate_to_datetime(article.get('published date')) if article.get('published date') else None

        articulos_info.append({
            "title": title_replaced,
            "description": description_replaced,
            "publisher": nombre_periodico['title'],
            "orientacion": nombre_periodico['alignment'],
            "url": article['url'],
            "published_date": published_date
        })

# Cargar el modelo y vectorizar los títulos
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
descripciones_embeddings = model.encode(descripciones)

# Configurar y aplicar DBSCAN para agrupar los artículos
clustering = DBSCAN(eps=eps, min_samples=min_sample, metric="cosine").fit(descripciones_embeddings)

# Crear un diccionario para almacenar los grupos de noticias
grupos_noticias = {}
for idx, label in enumerate(clustering.labels_):
    if label != -1:  # Ignorar puntos de ruido
        if label not in grupos_noticias:
            grupos_noticias[label] = []
        grupos_noticias[label].append(articulos_info[idx])

# Crear un diccionario para almacenar los artículos más recientes por tema y periódico
articulos_por_tema = {}


# Función para generar un tema basado en el título más corto
def generar_tema(grupo):
    return min((articulo["title"] for articulo in grupo), key=len)


# Guardar los artículos y temas en la base de datos
for label, grupo in grupos_noticias.items():
    if len(grupo) < min_sample:  # Solo proceder si hay al menos 4 artículos en el grupo
        continue

    topic = generar_tema(grupo)
    print(f'Tema generado: {topic}')

    for articulo in grupo:
        # Usar un diccionario para agrupar artículos por periódico y el tema
        key = (topic, articulo["publisher"])

        # Verificar si el tema y periódico ya están en el diccionario
        if key not in articulos_por_tema:
            articulos_por_tema[key] = articulo
        else:
            # Si ya existe un artículo, compararlo por fecha
            existing_article = articulos_por_tema[key]
            if articulo["published_date"] > existing_article["published_date"]:
                articulos_por_tema[key] = articulo  # Actualizar al más reciente

# Ahora guardar los artículos en la base de datos
for (topic, publisher), articulo in articulos_por_tema.items():
    # Verificar si el artículo ya existe en la base de datos
    if not NewsArticle.objects.filter(url=articulo["url"]).exists():
        # Obtener el periódico correspondiente
        try:
            periodico = Periodico.objects.get(title=articulo["publisher"])
        except Periodico.DoesNotExist:
            print(f"Periódico '{articulo['publisher']}' no encontrado. No se puede guardar el artículo.")
            continue

        # Crear y guardar el artículo en la base de datos con el tema asignado
        NewsArticle.objects.create(
            title=articulo["title"],
            publisher=periodico,  # Asocia el artículo con el objeto Periodico
            description=articulo["description"],
            topic=topic,
            url=articulo["url"],
            published_date=articulo["published_date"]
        )
