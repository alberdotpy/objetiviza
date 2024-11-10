from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from gnews import GNews
import django
import os
from collections import Counter
import re
from email.utils import parsedate_to_datetime
from collections import defaultdict


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'objetiviza.settings')
django.setup()
from noticias.models import Periodico, NewsArticle

# Inicializar GNews
google_news = GNews(language='es', country='ES', period='1d', max_results=5)

# Listas para almacenar datos de artículos
descripciones = []
articulos_info = []

newspapers = {
    'https://efe.com/': {
        'title': '- Agencia EFE',
        'alignment': 'Centro',
        'replace_words': '- EFE',
        'logo_url': 'https://elpais.com/favicon.ico'
    },
}


print(google_news.get_news_by_site('https://efe.com/'))
'''
# Obtener artículos por sitio de noticias
def get_articles(newspapers):
    for newspaper_url, nombre_periodico in newspapers.items():
        articles = google_news.get_news_by_site(newspaper_url)
        for article in articles:
            # Reemplazar palabras en el título y la descripción

            replace_words = nombre_periodico['replace_words']
            title_replaced = article['title'].replace(replace_words, '').strip()
            description_replaced = article['description'].replace(replace_words, '').strip() if article['description'] else ''
            descripciones.append(title_replaced)
            published_date = parsedate_to_datetime(article.get('published date')) if article.get('published date') else None
            full_article = get_full_article(article['url'])
            articulos_info.append({
                "title": title_replaced,
                "description": description_replaced,
                "publisher": nombre_periodico['title'],
                "orientacion": nombre_periodico['alignment'],
                "url": article['url'],
                "published_date": published_date,
                "full_article": full_article
            })
    #print(articulos_info)
    return articulos_info

def get_full_article(url):
    full_article = google_news.get_full_article(url)
    print(full_article)
    return full_article
'''


"""# Cargar el modelo y vectorizar los títulos
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
descripciones_embeddings = model.encode(descripciones)

# Configurar y aplicar DBSCAN para agrupar los artículos
clustering = DBSCAN(eps=0.3, min_samples=3, metric="cosine").fit(descripciones_embeddings)

# Crear un diccionario para almacenar los grupos de noticias
grupos_noticias = {}
for idx, label in enumerate(clustering.labels_):
    if label != -1:  # Ignorar puntos de ruido
        if label not in grupos_noticias:
            grupos_noticias[label] = []
        grupos_noticias[label].append(articulos_info[idx])

# Función para generar un tema basado en palabras clave
def generar_tema(grupo, max_palabras=4):
    all_titles = ' '.join(articulo["title"] for articulo in grupo)
    palabras = re.findall(r'\b\w+\b', all_titles.lower())
    palabras_filtradas = [palabra for palabra in palabras if len(palabra) > 2]
    palabra_frecuencia = Counter(palabras_filtradas)
    tema = ' '.join([palabra for palabra, _ in palabra_frecuencia.most_common(max_palabras)])
    return tema.title()

# Guardar los artículos y temas en la base de datos
for label, grupo in grupos_noticias.items():
    # Generar un tema representativo para el grupo
    topic2 = generar_tema(grupo)
    print(topic2)
    topic = min((articulo["title"] for articulo in grupo), key=len)[:100]  # Limitar a 100 caracteres
    print(topic)

    for articulo in grupo:
        print(grupo, articulo)"""
