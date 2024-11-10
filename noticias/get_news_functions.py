import datetime
import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser


def obtener_base_url(url):
    # Expresión regular para extraer solo la base de la URL
    pattern = r'^(https?://[^/]+)'
    match = re.match(pattern, url)
    return match.group(1) if match else None


def get_feed(rss_url):
    # Definir un User-Agent personalizado para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar una solicitud GET al RSS con el User-Agent personalizado
    response = requests.get(rss_url, headers=headers)

    if response.status_code == 200:
        # Parsear el contenido del feed RSS
        feed = feedparser.parse(response.text)

        # Mostrar el título del feed y la descripción
        #print("Título del Feed:", feed.feed.title)
        #print("Link:", feed.feed.link)

        print(feed.entries[0])
        descripcion = obtener_descripcion_rss(feed.entries[0])
        if not descripcion:
            descripcion = obtener_subtitulo_rss(feed.entries[0])
        print("Descripción:", descripcion)
        print(len(feed.entries))

        # Recorrer las entradas del feed
        """for entry in feed.entries:
            print(entry)
            print("\nTítulo:", entry.title)
            print("Descripción:", entry.description)
            print("Link:", entry.link)
            # Convertir la fecha de publicación
            if 'published' in entry:
                print("Fecha de Publicación:", entry.published)
            elif 'updated' in entry:
                print("Fecha de Publicación:", entry.updated)
            else:
                pass
            if 'tags' in entry:
                keywords = [tag.term for tag in entry.tags]
                print("Palabras clave:", ", ".join(keywords))
            else:
                print("Palabras clave: No disponibles")

            # Extraer la imagen, si está disponible en 'media_content'
            if 'media_content' in entry:
                # Verificamos que la lista 'media_content' no esté vacía
                if len(entry.media_content) > 0:
                    # Obtenemos la URL de la imagen (especificada en la primera posición)
                    image_url = entry.media_content[0].get('url', None)
                    if image_url:
                        print("Imagen URL:", image_url)
                    else:
                        print("Imagen no disponible")
                else:
                    print("No se encontró imagen en el feed.")
            else:
                print("No hay contenido multimedia disponible.")"""
    else:
        print(f"Error al obtener el feed. Código de estado: {response.status_code}")


def extraer_noticias(url):
    response = requests.get(url)
    response.raise_for_status()  # Verifica que la solicitud fue exitosa
    base_url = obtener_base_url(url)

    # Parsear el HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lista para almacenar las noticias
    noticias = []

    # Encontrar los elementos de las noticias (esto depende de la estructura HTML)
    for item in soup.find_all('article'):
        print(item)
        titulo = obtener_titulo(item, url)

        link = item.find('a')['href'] if item.find('a') else "#"

        if link.startswith('/'):
            link = base_url + link

        descripcion = obtener_descripcion(item)

        imagen = obtener_imagen(item)

        # Extraer la fecha de publicación desde la etiqueta <meta itemprop="datePublished">
        fecha_pub = None
        meta_fecha = soup.find('meta', itemprop='datePublished')

        if meta_fecha:
            fecha_pub = meta_fecha.get('content', None)

        time_element = item.find('time', {'datetime': True})
        if time_element:
            fecha_pub = time_element['datetime']


        # Intentar extraer tags (si existen)
        tags = []
        tag_elements = item.find_all('a', {'class': 'tag-class'})  # Ajustar según la clase correcta en la página
        if tag_elements:
            tags = [tag.get_text(strip=True) for tag in tag_elements]

        # Añadir la noticia a la lista
        noticias.append({
            'titulo': titulo,
            'link': link,
            'descripcion': descripcion,
            'fecha_pub': fecha_pub if fecha_pub else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z"),
            'tags': tags,
            'imagen': imagen
        })

    return noticias


def obtener_titulo(item, url):
    titulo = item.find('h2').get_text(strip=True) if item.find('h2') else ""
    titulo = item.find('h3').get_text(strip=True) if not titulo else ""

    # Check for 'efe' in the URL and extract the title accordingly
    if 'efe' in url:
        h2_tag = item.find('h2', class_='entry-title')  # Check for the h2 with class 'entry-title'
        if h2_tag:
            a_tag = h2_tag.find('a')  # Find the <a> tag within the h2
            if a_tag:
                titulo = a_tag.get_text(strip=True)  # Get the title text from the <a> tag

    # Existing checks for other sources
    if 'elespanol' in url:
        h2_tag = item.find('h2', class_='art__title')
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag:
                titulo = a_tag.get_text(strip=True)

    if 'larazon' in url:
        header_tag = item.find('h2', class_='article__title')
        if header_tag:
            a_tag = header_tag.find('a')
            if a_tag:
                titulo = a_tag.get_text(strip=True)

    if 'huffington' in url:
        h2_tag = item.find('h2', class_='c-article__title')
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag:
                titulo = a_tag.get_text(strip=True)
        if not titulo:
            a_tag = item.find('a', class_='c-article__imghref')
            if a_tag:
                titulo = a_tag.get('title', '').strip()

    return titulo


def obtener_descripcion(item):
    descripcion = item.find('p').get_text(strip=True) if item.find('p') else ""
    if not descripcion:
        descripcion_div = item.find('div', itemprop='description')
        descripcion = descripcion_div.get_text(strip=True) if descripcion_div else ""
    return descripcion


def obtener_imagen(item):
    # Extraer imagen
    imagen = None

    # Primero, intenta obtener el 'src'
    if item.find('img'):
        imagen = item.find('img').get('src')

        # Si no hay 'src', intenta obtener 'data-src'
        if not imagen:
            data_src = item.find('img').get('data-src')
            if data_src:
                try:
                    data_src_list = json.loads(data_src)
                    if isinstance(data_src_list, list) and data_src_list:
                        imagen = data_src_list[0]  # Usa la primera URL en la lista
                except json.JSONDecodeError:
                    print("Error al decodificar data-src")
    return imagen


def obtener_fecha(item):
    # Extraer la fecha de publicación desde la etiqueta <meta itemprop="datePublished">
    fecha_pub = None
    meta_fecha = item.find('meta', itemprop='datePublished')
    time_element = item.find('time', {'datetime': True})

    if meta_fecha:
        fecha_pub = meta_fecha.get('content', None)

    elif time_element:
        fecha_pub = time_element['datetime']

    else:
        fecha_pub = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return fecha_pub


def obtener_descripcion_rss(entry):
    description = entry.description
    soup = BeautifulSoup(entry.description, 'html.parser')
    p_tag = soup.find_all('p')
    if p_tag:
        description = ' '.join(p.get_text(strip=True) for p in p_tag)
    description_replaced = description.split("&nbsp;")[0] if entry.description else ''
    return description_replaced


def obtener_subtitulo_rss(entry):
    description = entry.description
    soup = BeautifulSoup(entry.description, 'html.parser')
    subtitles = soup.find('p', class_='subtitle')
    if subtitles:
        description = subtitles.get_text(strip=True)
    description_replaced = description.split("&nbsp;")[0] if entry.description else ''
    return description_replaced


'''
noticias_extraidas = get_feed('https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml')

# Mostrar las noticias extraídas
for noticia in noticias_extraidas:
    print("Título:", noticia['titulo'])
    print("Descripción:", noticia['descripcion'])
    print("Link:", noticia['link'])
    print("Fecha de Publicación:", noticia['fecha_pub'])
    print("Tags:", ", ".join(noticia['tags']) if noticia['tags'] else "No disponibles")
    print("Imagen:", noticia['imagen'])
    print("-" * 80)
'''