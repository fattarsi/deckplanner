"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from deckplanner import views


router = routers.DefaultRouter()
router.register(r'collections', views.CollectionViewSet)
router.register(r'decks', views.DeckViewSet)
router.register(r'cards', views.CardViewSet)
router.register(r'deckimport', views.DeckImportViewSet, basename='deckimport')

urlpatterns = [
    path('api/decks/<int:deck_id>/planner', views.DeckPlannerView.as_view(), name='deck-planner'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('', views.home, name='deck-dashboard'),
]
