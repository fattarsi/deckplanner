from django.shortcuts import render, get_object_or_404

from rest_framework import views, viewsets, response, status
from rest_framework import pagination
from rest_framework import parsers
from rest_framework import renderers

from deckplanner import models
from deckplanner import serializers
from deckplanner import deck_utils


def home(request):
    """
    Render the main dashboard page.
    The template will load the deck data asynchronously.
    """
    total_cards = models.Card.objects.count()
    available_cards = models.Card.objects.filter(deck__isnull=True).count()
    cards_in_decks = models.Card.objects.filter(deck__isnull=False).count()

    return render(
        request,
        'index.html',
        {
            'total_cards': total_cards,
            'available_cards': available_cards,
            'cards_in_decks': cards_in_decks,
        },
    )
    return render(request, 'index.html')

def deck_detail(request, deck_id):
    return render(request, 'deck_detail.html', {'deck_id': deck_id})

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

    def get(self, request, deck_id, *args, **kw):
        deck = get_object_or_404(models.Deck, pk=deck_id)

        cards = deck.cards.all()

        ci = deck_utils.get_color_identity(cards)

        # cards not in any deck with compatible color identity
        ac = models.Card.objects.exclude(oracle_card__type_line__startswith='Basic Land')
        ac = ac.filter(
            oracle_card__color_identity__contained_by=ci.split(','),
            deck__isnull=True).order_by('oracle_card__edhrec_rank')

        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(ac, request)

        s = serializers.CardSerializer(page, many=True)
        return paginator.get_paginated_response(s.data)
