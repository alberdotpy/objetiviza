lst_no_rss = ['La Razón', 'El Español', 'Agencia EFE', 'Huffington Post', 'Vozpópuli', 'El Plural']

rss_espana = {
    'El País': {
        'international': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada',
        'spain': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada',
        'economy': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/economia/portada',
        'sport': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/deportes/portada',
        'science': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/ciencia/portada',
    },
    'Infolibre': {
        'international': 'https://www.infolibre.es/rss/internacional',
        'spain': 'https://www.infolibre.es/rss/politica',
        'economy': 'https://www.infolibre.es/rss/economia',
        'science': 'https://www.infolibre.es/rss/ciencia',
    },
    'El Plural': {
        'international': 'https://www.elplural.com/politica/internacional',
        'spain': 'https://www.elplural.com/politica/espana',
        'economy': 'https://www.elplural.com/economia',
        'science': 'https://www.elplural.com/leequid/ciencia',
    },
    'Newtral': {
        'international': 'https://www.newtral.es/seccion/internacional/feed/',
        'spain': 'https://www.newtral.es/seccion/politica/feed/',
        'economy': 'https://www.newtral.es/seccion/economia/feed/',
        'science': 'https://www.newtral.es/seccion/ciencia/feed/',
    },
    'El Mundo': {
        'international': 'https://e00-elmundo.uecdn.es/elmundo/rss/internacional.xml',
        'spain': 'https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml',
        'economy': 'https://e00-elmundo.uecdn.es/elmundo/rss/economia.xml',
        'sport': 'https://e00-elmundo.uecdn.es/elmundodeporte/rss/portada.xml',
        'science': 'https://e00-elmundo.uecdn.es/elmundo/rss/ciencia.xml',
    },
    'El Español': {
        'international': 'https://www.elespanol.com/mundo/',
        'spain': 'https://www.elespanol.com/espana/',
        'economy': 'https://www.elespanol.com/invertia/',
        'sport': 'https://www.elespanol.com/deportes/',
        'science': 'https://www.elespanol.com/ciencia/',
    },
    'ABC': {
        'international': 'https://www.abc.es/rss/atom/internacional/',
        'spain': 'https://www.abc.es/rss/atom/espana/',
        'economy': 'https://www.abc.es/rss/atom/economia/',
        'sport': 'https://www.abc.es/rss/atom/deportes/',
        'science': 'https://www.abc.es/rss/atom/ciencia/',
    },
    'La Vanguardia': {
        'international': 'https://www.lavanguardia.com/rss/internacional.xml',
        'spain': 'https://www.lavanguardia.com/rss/politica.xml',
        'economy': 'https://www.lavanguardia.com/rss/economia.xml',
        'sport': 'https://www.lavanguardia.com/rss/deportes.xml',
        'science': 'https://www.lavanguardia.com/rss/tecnologia.xml',
    },
    'La Razón': {
        'international': 'https://www.larazon.es/internacional/',
        'spain': 'https://www.larazon.es/espana/',
        'economy': 'https://www.larazon.es/economia/',
        'sport': 'https://www.larazon.es/deportes/',
        'science': 'https://www.larazon.es/ciencia/',
    },
    'El Confidencial': {
        'international': 'https://rss.elconfidencial.com/mundo/',
        'spain': 'https://rss.elconfidencial.com/espana/',
        'economy': 'https://rss.elconfidencial.com/mercados/',
        'sport': 'https://rss.elconfidencial.com/deportes/',
        'science': 'https://rss.elconfidencial.com/tecnologia/',
    },
    'Público': {
        'international': 'https://www.publico.es/rss/internacional',
        'spain': 'https://www.publico.es/rss/espana',
        'economy': 'https://www.publico.es/rss/economia',
        'sport': 'https://www.publico.es/rss/deportes',
        'science': 'https://www.publico.es/rss/ciencias',
    },
    'El Periódico': {
        'international': 'https://www.elperiodico.com/es/rss/internacional/rss.xml',
        'spain': 'https://www.elperiodico.com/es/rss/politica/rss.xml',
        'economy': 'https://www.elperiodico.com/es/rss/economia/rss.xml',
        'sport': 'https://www.elperiodico.com/es/rss/deportes/rss.xml',
        'science': 'https://www.elperiodico.com/es/rss/ciencia/rss.xml',
    },
    'RTVE': {
        'international': 'http://api2.rtve.es/rss/temas_mundo.xml',
        'spain': 'http://api2.rtve.es/rss/temas_espana.xml',
        'economy': 'http://api2.rtve.es/rss/temas_economia.xml',
        'sport': 'http://api2.rtve.es/rss/temas_deportes.xml',
        'science': 'http://api2.rtve.es/rss/temas_ciencia-tecnologia.xml',
    },
    '20 Minutos': {
        'international': 'https://www.20minutos.es/rss/internacional/',
        'spain': 'https://www.20minutos.es/rss/nacional/',
        'sport': 'https://www.20minutos.es/rss/deportes/',
        'science': 'https://www.20minutos.es/rss/ciencia/',
    },
    'El Diario': {
        'international': 'https://www.eldiario.es/rss/internacional',
        'spain': 'https://www.eldiario.es/rss/politica',
        'economy': 'https://www.eldiario.es/rss/economia',
        'science': 'https://www.eldiario.es/rss/ciencia',
    },
    'Huffington Post': {
        'international': 'https://www.huffingtonpost.es/global?int=submenu_2',
        'spain': 'https://www.huffingtonpost.es/politica?int=submenu_1',
    },
    'OK Diario': {
        'international': ['https://okdiario.com/feed', 'internacional'],
        'spain': ['https://okdiario.com/feed', 'espana'],
        'economy': ['https://okdiario.com/feed', 'economia'],
        'sport': ['https://okdiario.com/feed', 'deportes'],
        'science': ['https://okdiario.com/feed', 'ciencia'],
    },
    'Heraldo': {
        'international': 'https://www.heraldo.es/rss/internacional/',
        'spain': 'https://www.heraldo.es/rss/nacional/',
        'economy': 'https://www.heraldo.es/rss/economia/',
        'sport': 'https://www.heraldo.es/rss/deportes/',
    },
    'Agencia EFE': {
        'international': 'https://efe.com/mundo/',
        'spain': 'https://efe.com/espana/',
        'economy': 'https://efe.com/economia/',
        'sport': 'https://efe.com/deportes/',
        'science': 'https://efe.com/ciencia-y-tecnologia/',
    },
    'CNN en Español': {
        'international': 'https://cnnespanol.cnn.com/seccion/mundo/feed/',
        'spain': 'https://cnnespanol.cnn.com/seccion/espana/feed/',
        'economy': 'https://cnnespanol.cnn.com/seccion/economia/feed/',
        'sport': 'https://cnnespanol.cnn.com/seccion/deportes/feed/',
        'science': 'https://cnnespanol.cnn.com/seccion/ciencia/feed/',
    },
    'Euronews Español': {
        'international': 'https://es.euronews.com/rss',
    },
    'Europa Press': {
        'international': 'https://www.europapress.es/internacional/',
        'spain': 'https://www.europapress.es/nacional/',
        'economy': 'https://www.europapress.es/economia/',
        'sport': 'https://www.europapress.es/deportes/',
    },
    'DW (Español)': {
        'international': 'https://rss.dw.com/rdf/rss-sp-inter',
        'economy': 'https://rss.dw.com/rdf/rss-sp-eco',
        'science': 'https://rss.dw.com/rdf/rss-sp-cyt',
    },
    'elEconomista': {
        'economy': 'https://www.eleconomista.es/rss/rss-seleccion-ee.php',
    },
    'Vozpópuli': {
        'international': 'https://www.vozpopuli.com/internacional/',
        'spain': 'https://www.vozpopuli.com/espana/',
        'economy': 'https://www.vozpopuli.com/economia/',
    },
    'Expansión': {
        'economy': 'https://e00-expansion.uecdn.es/rss/portada.xml',
    },
    'Bolsamania': {
        'economy': 'https://www.bolsamania.com/rss/generarRss2.php',
    },
    'Cinco Días': {
        'economy': 'https://cincodias.elpais.com/rss/cincodias/noticias_mas_vistas.xml',
    },
    'Estrategias de inversión': {
        'economy': 'https://www.estrategiasdeinversion.com/rss/rssnoticias.xml',
    },
    'FRANCE 24 Español': {
        'international': 'https://www.france24.com/es/rss',
        'economy': 'https://www.france24.com/es/eco-tecno/rss',
        'sport': 'https://www.france24.com/es/deportes/rss',
    },
}
