# urls.py
from django.urls import path
from .views import home_view, articles_view, statistics_view, contact_view

urlpatterns = [
    path('', home_view, name='home'),
    path('statistics/', statistics_view, name='statistics'),
    path('contact/', contact_view, name='contact'),
    path('<str:section>/', articles_view, name='articles'),
]
