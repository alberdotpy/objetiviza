import django
import os
import feedparser
import requests
from get_news_functions import obtener_titulo, obtener_descripcion, obtener_imagen, obtener_fecha
from get_news_functions import obtener_descripcion_rss, obtener_subtitulo_rss
from dateutil import parser
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from collections import defaultdict
from RSS import rss_espana, lst_no_rss

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'objetiviza.settings')
django.setup()

from noticias.models import NewsArticle, Periodico

# Parámetros de filtrado
exclude_keywords = ['noticias', 'programación tv', 'horóscopo', 'guía de tv', 'sudoku', 'crucigrama', 'directo',
                    'en imágenes', 'el tiempo', 'meteo', 'esquelas', 'última hora', 'resumen, goles', 'horario y',
                    'bonoloto', 'sorteo', 'AEMET', 'pronóstico', 'información del ejecutivo', 'informativo',
                    'informatiu', 'crónica', 'Research and analysis']
min_words_in_title = 4


def get_topics_from_db(eps, min_publishers, section):
    # Cargar el modelo de embeddings
    models = ["sentence-transformers/paraphrase-MiniLM-L6-v2", "sentence-transformers/all-mpnet-base-v2", "sentence-transformers/all-MiniLM-L6-v2"]
    model = SentenceTransformer(models[1])

    # Obtener todos los artículos de la base de datos
    articles = NewsArticle.objects.filter(publisher__visible=True, section=section).select_related('publisher').all()
    print(f"Total de artículos encontrados: {len(articles)}")

    # Crear listas para almacenar los títulos y la información de los artículos
    titles = []
    article_info = []

    for article in articles:
        # Almacenar el título modificado y la información del artículo
        titles.append(article.title + " ; " + article.description)
        #titles.append(article.title)
        article_info.append({
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "section": article.section,
            "url": article.url,
            "published_date": article.published_date,
            "publisher": article.publisher.title
        })

    # Generar embeddings de los títulos modificados
    title_embeddings = model.encode(titles)

    # Configurar y aplicar DBSCAN para agrupar los artículos
    clustering = DBSCAN(eps=eps, min_samples=3, metric="cosine").fit(title_embeddings)

    # Crear diccionario para almacenar los grupos de temas
    topic_groups = defaultdict(list)

    # Agrupar artículos por etiquetas de DBSCAN
    for idx, label in enumerate(clustering.labels_):
        if label != -1:  # Ignorar puntos de ruido
            topic_groups[label].append(article_info[idx])

    # Filtrar clusters por diversidad de publishers
    filtered_topic_groups = {}
    for label, group in topic_groups.items():
        # Obtener la cantidad de publishers únicos en el grupo
        publishers = {art['publisher'] for art in group}
        # Filtrar solo los temas con al menos `min_publishers` diferentes
        if len(publishers) >= min_publishers:
            filtered_topic_groups[label] = group

    # Crear temas para cada grupo y actualizar la base de datos
    for label, group in filtered_topic_groups.items():
        # Seleccionar el título más corto del grupo para usarlo como título del tema
        topic_title = min((art["title"] for art in group), key=len)

        print(f"Tema: {topic_title}")

        # Actualizar el campo `topic` de cada artículo en el grupo
        for article in group:
            article_obj = NewsArticle.objects.get(id=article["id"])
            article_obj.topic = topic_title
            article_obj.save()

        print(f"Tema '{topic_title}' asignado a {len(group)} artículos.")

    print("Agrupación y asignación de temas completada.")


def get_feed(rss_url, periodico_title, section):
    # Definir un User-Agent personalizado para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar una solicitud GET al RSS con el User-Agent personalizado
    response = requests.get(rss_url, headers=headers)

    feed = feedparser.parse(response.text)

    # Obtener el periódico desde el RSS
    periodico_url = feed.feed.link
    periodico, created = Periodico.objects.get_or_create(title=periodico_title)

    # Recorrer las entradas del feed
    for entry in feed.entries:
        # Filtrar artículos que contengan palabras clave excluidas
        if any(keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower() for keyword in exclude_keywords):
            continue

        # Reemplazar palabras en el título
        title_replaced = entry.title.replace(periodico.replace_words, '').strip()
        title_word_count = len(title_replaced.split())
        if title_word_count < min_words_in_title:
            continue

        # Reemplazar palabras en la descripción
        description = obtener_descripcion_rss(entry)
        if not description:
            description = obtener_subtitulo_rss(entry)

        # Convertir la fecha de publicación
        if 'published' in entry:
            published_date = parser.parse(entry.published)
        elif 'updated' in entry:
            published_date = parser.parse(entry.updated)
        else:
            published_date = None

        imagen = None
        if 'media_content' in entry:
            # Verificamos que la lista 'media_content' no esté vacía
            if len(entry.media_content) > 0:
                # Obtenemos la URL de la imagen (especificada en la primera posición)
                imagen = entry.media_content[0].get('url', None)

        add_to_database(entry.link, title_replaced, periodico, description, published_date, section, imagen)


def extract_news(url, periodico_title, section):
    response = requests.get(url)
    response.raise_for_status()  # Verifica que la solicitud fue exitosa

    soup = BeautifulSoup(response.text, 'html.parser')

    periodico, created = Periodico.objects.get_or_create(title=periodico_title)

    noticias = []

    for item in soup.find_all('article'):
        titulo = obtener_titulo(item, url)

        descripcion = obtener_descripcion(item)

        link = item.find('a')['href'] if item.find('a') else "#"
        if link.startswith('/'):
            link = periodico.url + link

        fecha_pub = obtener_fecha(item)

        imagen = obtener_imagen(item)

        # Intentar extraer tags (si existen)
        tags = []
        tag_elements = item.find_all('a', {'class': 'tag-class'})  # Ajustar según la clase correcta en la página
        if tag_elements:
            tags = [tag.get_text(strip=True) for tag in tag_elements]

        add_to_database(link, titulo, periodico, descripcion, fecha_pub, section, imagen)


def get_news_from_sites(limit=None):
    # Obtener los periódicos de la base de datos, limitando el número si se especifica
    periodicos = Periodico.objects.filter(visible=True)[:limit] if limit else Periodico.objects.filter(visible=True)

    # Obtener artículos por cada periódico
    for periodico in periodicos:
        try:
            # Comprobar si el periódico tiene RSS o no
            categories = rss_espana.get(periodico.title)
            if periodico.title not in lst_no_rss:
                for category, rss_url in categories.items():
                    print(f"Obteniendo noticias de {periodico.title} - {category}")
                    get_feed(rss_url, periodico.title, category)
            else:
                for category, rss_url in categories.items():
                    print(f"Extrayendo noticias de {periodico.title} - {category}")
                    extract_news(rss_url, periodico.title, category)
        except:
            print(f"Error con {periodico.title} - {category} - {rss_url}")


def add_to_database(link, titulo, periodico, descripcion, fecha_pub, section, imagen):
    # Verificar si el artículo ya existe en la base de datos
    if not NewsArticle.objects.filter(url=link).exists():
        NewsArticle.objects.create(
            title=titulo,
            publisher=periodico,
            description=descripcion,
            url=link,
            published_date=fecha_pub,
            section=section,
            image_url=imagen
        )


#get_feed('https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada', 'El País', 'international')

#get_news_from_topics()
get_news_from_sites()
#assign_section_from_db(confidence=0.6)
get_topics_from_db(eps=0.23, min_publishers=3, section="spain")
get_topics_from_db(eps=0.23, min_publishers=3, section="international")
get_topics_from_db(eps=0.22, min_publishers=3, section="economy")
get_topics_from_db(eps=0.21, min_publishers=3, section="sport")
get_topics_from_db(eps=0.23, min_publishers=3, section="science")
