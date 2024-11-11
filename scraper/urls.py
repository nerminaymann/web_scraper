from django.urls import path
from .views import ScraperView

urlpatterns = [
    path('scrape/', ScraperView.as_view(), name='scrape'),
]
