from django.shortcuts import render

from rest_framework import views, viewsets, response, status
from rest_framework import pagination
from rest_framework import parsers
from rest_framework import renderers

from deckplanner import models
from deckplanner import serializers
from deckplanner import deck_utils


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
        s.save()
        return response.Response(s.data, status=status.HTTP_201_CREATED)

class DeckPlannerView(views.APIView):
    serializer_class = serializers.DeckPlannerSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request):
        s = serializers.DeckPlannerSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        cards = s.validated_data['deck_list']
        ci = deck_utils.get_color_identity(cards)

        # cards not in any deck with compatible color identity
        ac = models.Card.objects.filter(deck__isnull=True)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(ac, request)

        s = serializers.CardSerializer(ac, many=True)
        return paginator.get_paginated_response(s.data)
