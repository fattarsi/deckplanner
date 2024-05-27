from django.shortcuts import render

from rest_framework import viewsets, response, status

from deckplanner import models
from deckplanner import serializers


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = models.Collection.objects.all()
    serializer_class = serializers.CollectionSerializer

class DeckViewSet(viewsets.ModelViewSet):
    queryset = models.Deck.objects.all()
    serializer_class = serializers.DeckSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = models.Card.objects.all()
    serializer_class = serializers.CardSerializer

class DeckImportViewSet(viewsets.ViewSet):
    serializer_class = serializers.DeckImportSerializer

    def list(self, request):
        qs = models.Deck.objects.all()
        s = serializers.DeckListSerializer(qs, many=True)
        return response.Response(s.data)

    def create(self, request):
        s = serializers.DeckImportSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save(s)
        return response.Response(s.data, status=status.HTTP_201_CREATED)
