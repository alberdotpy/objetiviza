from django.shortcuts import render
from .models import NewsArticle, Periodico
from collections import defaultdict
from django.utils.text import slugify

def home_view(request):
    articles = NewsArticle.objects.all()
    # Cuenta los artículos para cada sección
    articles_count = articles.count()
    spain_count = NewsArticle.objects.filter(section='spain').count()
    international_count = NewsArticle.objects.filter(section='international').count()
    economy_count = NewsArticle.objects.filter(section='economy').count()
    science_count = NewsArticle.objects.filter(section='science').count()
    sports_count = NewsArticle.objects.filter(section='sport').count()

    # Pasar los conteos en el contexto
    context = {
        'total_count': articles_count,
        'spain_count': spain_count,
        'international_count': international_count,
        'economy_count': economy_count,
        'science_count': science_count,
        'sports_count': sports_count,
    }

    return render(request, 'index.html', context)


def contact_view(request):
    return render(request, 'contact.html')


def articles_view(request, section):
    # Obtener filtros de la solicitud
    selected_publishers = request.GET.getlist('publishers')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Filtrar artículos por sección y visibilidad del periódico
    articles = NewsArticle.objects.filter(
        topic__isnull=False,
        section=section,
        publisher__visible=True
    ).order_by('-published_date')

    # Aplicar filtros si están presentes
    if selected_publishers:
        articles = articles.filter(publisher__title__in=selected_publishers)
    if start_date:
        articles = articles.filter(published_date__gte=start_date)
    if end_date:
        articles = articles.filter(published_date__lte=end_date)

    topics = set(article.topic for article in articles)

    # Estructura para agrupar artículos por tema
    grouped_articles = defaultdict(lambda: {
        'articles': [],
        'publishers': set(),
        'left_percentage': 0,
        'center_left_percentage': 0,
        'center_percentage': 0,
        'center_right_percentage': 0,
        'right_percentage': 0,
    })

    # Llenar grouped_articles con artículos y contar alineaciones ideológicas
    for article in articles:
        grouped_articles[article.topic]['articles'].append(article)
        grouped_articles[article.topic]['publishers'].add(article.publisher.title)

    # Ordenar y calcular porcentajes de alineación ideológica
    sorted_grouped_articles = sorted(grouped_articles.items(), key=lambda item: len(item[1]['publishers']), reverse=True)

    for topic, data in grouped_articles.items():
        # Contadores de alineaciones ideológicas
        left_count = sum(1 for article in data['articles'] if article.publisher.alignment.lower() == 'izquierda')
        center_left_count = sum(1 for article in data['articles'] if article.publisher.alignment.lower() == 'centro-izquierda')
        center_count = sum(1 for article in data['articles'] if article.publisher.alignment.lower() == 'centro')
        center_right_count = sum(1 for article in data['articles'] if article.publisher.alignment.lower() == 'centro-derecha')
        right_count = sum(1 for article in data['articles'] if article.publisher.alignment.lower() == 'derecha')
        total_count = left_count + center_left_count + center_count + center_right_count + right_count

        # Calcular porcentaje de cada alineación
        if total_count > 0:
            data['left_percentage'] = (left_count / total_count) * 100
            data['center_left_percentage'] = (center_left_count / total_count) * 100
            data['center_percentage'] = (center_count / total_count) * 100
            data['center_right_percentage'] = (center_right_count / total_count) * 100
            data['right_percentage'] = (right_count / total_count) * 100

    # Obtener lista de todos los periódicos para opciones de filtro
    all_publishers = Periodico.objects.filter(visible=True)

    # Seleccionar plantilla según la sección
    template_name = f'articles.html'

    if section == 'international':
        nombre_seccion = 'Actualidad Internacional'
    elif section == 'spain':
        nombre_seccion = 'Espana'
    elif section == 'sport':
        nombre_seccion = 'Deportes'
    elif section == 'economy':
        nombre_seccion = 'Economía'
    elif section == 'science':
        nombre_seccion = 'Ciencia'

    # Renderizar template con artículos agrupados y filtros
    return render(request, template_name, {
        'nombre_seccion': nombre_seccion,
        'grouped_articles': dict(sorted_grouped_articles),
        'all_publishers': all_publishers,  # opciones de filtro
        'selected_publishers': selected_publishers,  # filtro aplicado
        'start_date': start_date,
        'end_date': end_date,
        'topics': [slugify(topic) for topic in topics],
    })


def statistics_view(request):
    periodicos = Periodico.objects.filter(visible=True)
    articulos = NewsArticle.objects.filter(publisher__visible=True)

    # Inicializar contadores
    total_periodicos = periodicos.count()
    articulos_por_periodico = defaultdict(int)
    periodicos_por_ideologia = defaultdict(int)
    periodicos_info = {}

    for periodico in periodicos:
        periodicos_por_ideologia[periodico.alignment] += 1

    # Calcular el porcentaje para cada ideología
        # Calcular el porcentaje para cada ideología
        periodicos_por_ideologia_porcentaje = {
            'Izquierda': (periodicos_por_ideologia.get('Izquierda', 0) / total_periodicos) * 100,
            'Centro-Izquierda': (periodicos_por_ideologia.get('Centro-Izquierda', 0) / total_periodicos) * 100,
            'Centro': (periodicos_por_ideologia.get('Centro', 0) / total_periodicos) * 100,
            'Centro-Derecha': (periodicos_por_ideologia.get('Centro-Derecha', 0) / total_periodicos) * 100,
            'Derecha': (periodicos_por_ideologia.get('Derecha', 0) / total_periodicos) * 100,
        }

    # Contar artículos por periódico e ideología
    for articulo in articulos:
        articulos_por_periodico[articulo.publisher.title] += 1

        publisher = articulo.publisher
        if publisher.title not in periodicos_info:
            periodicos_info[publisher.title] = {
                'url': publisher.url,
                'logo_url': publisher.logo_url,
                'alignment': publisher.alignment,
                #'readers': publisher.readers,
                #'budget': publisher.budget,
                #'region': publisher.region,
                'articulos_count': articulos_por_periodico[publisher.title],
            }
        else:
            periodicos_info[publisher.title]['articulos_count'] = articulos_por_periodico[publisher.title]

    periodicos_info = sorted(periodicos_info.items(), key=lambda item: int(item[1]['articulos_count']), reverse=True)

    context = {
        'total_periodicos': total_periodicos,
        'periodicos_count': dict(periodicos_por_ideologia),
        'periodicos_count_percentage': periodicos_por_ideologia_porcentaje,
        'periodicos_info': dict(periodicos_info),
    }

    return render(request, 'statistics.html', context=context)
