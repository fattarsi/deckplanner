from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from rest_framework import views, viewsets, response, status
from rest_framework import filters
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        # Check params manually
        if self.request.query_params.get('color_identity'):
            qs = qs.filter(oracle_card__color_identity__icontains=self.request.query_params['color_identity'])
        if self.request.query_params.get('cmc'):
            qs = qs.filter(oracle_card__cmc=self.request.query_params['cmc'])
        if self.request.query_params.get('deck__isnull') == 'True':
            qs = qs.filter(deck__isnull=True)
        return qs

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

    def get_queryset(self):
        qs = models.Card.objects.exclude(oracle_card__type_line__startswith='Basic Land')
        qs = qs.filter(deck__isnull=True)


        search = self.request.query_params.get('search')
        supertype = self.request.query_params.get('supertype')
        cmc = self.request.query_params.get('cmc')
        color = self.request.query_params.get('color')
        oracle_text = self.request.query_params.get('oracle_text')
        type_line = self.request.query_params.get('type_line')

        if search:
            qs = qs.filter(name__icontains=search)

        if supertype:
            # filter by supertype (before " —")
            qs = qs.filter(
                Q(oracle_card__type_line__istartswith=supertype) |
                Q(oracle_card__type_line__istartswith='Legendary ' + supertype)
            )

        if cmc:
            if cmc == "5+":
                qs = qs.filter(oracle_card__cmc__gte=5)
            else:
                qs = qs.filter(oracle_card__cmc=float(cmc))

        if color:
            # color_identity is a list on oracle_card; this assumes you store it as arrayfield
            qs = qs.filter(oracle_card__color_identity__contains=[color])

        if oracle_text:
            qs = qs.filter(oracle_card__oracle_text__icontains=oracle_text)
        if type_line:
            qs = qs.filter(oracle_card__type_line__icontains=type_line)

        return qs.order_by('name')  # optional ordering

    def get(self, request, deck_id, *args, **kw):
        deck = get_object_or_404(models.Deck, pk=deck_id)

        cards = deck.cards.all()

        ci = deck_utils.get_color_identity(cards)

        # cards not in any deck with compatible color identity
        ac = self.get_queryset()
        ac = ac.filter(oracle_card__color_identity__contained_by=ci).order_by('oracle_card__edhrec_rank')

        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(ac, request)

        s = serializers.CardSerializer(page, many=True)
        return paginator.get_paginated_response(s.data)

class DeckUpdateCardsView(views.APIView):
    def post(self, request, deck_id):
        deck = get_object_or_404(models.Deck, id=deck_id)
        data = request.data
        add_ids = data.get('add_ids', [])
        remove_ids = data.get('remove_ids', [])
        # Remove cards
        if remove_ids:
            models.Card.objects.filter(id__in=remove_ids, deck=deck).update(deck=None)
        # Add cards
        if add_ids:
            models.Card.objects.filter(id__in=add_ids).update(deck=deck)
        return response.Response({"message": "Changes committed."}, status=status.HTTP_200_OK)
