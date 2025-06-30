from collections import namedtuple

from django import urls

from rest_framework import serializers

from deckplanner import models, deck_utils


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['name']

class OracleCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OracleCard
        fields = ['id', 'cmc', 'type_line', 'color_identity', 'set_code', 'collector_number', 'rarity', 'edhrec_rank']


class CardSerializer(serializers.ModelSerializer):
    oracle_card = OracleCardSerializer(many=False, read_only=True)

    class Meta:
        model = models.Card
        fields = ['id', 'name', 'oracle_card']

class DeckSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='deck-detail', lookup_field='pk')
    planner_url = serializers.SerializerMethodField()
    cards = CardSerializer(many=True, read_only=True)
    card_count = serializers.IntegerField(source='cards.count', read_only=True)
    card_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    def get_planner_url(self, obj):
        request = self.context.get('request')
        path = urls.reverse('deck-planner', kwargs={'deck_id': obj.pk})
        return request.build_absolute_uri(path)

    def create(self, validated_data):
        card_ids = validated_data.pop('card_ids', [])
        deck = super().create(validated_data)
        if card_ids:
            # assign selected cards to this new deck
            models.Card.objects.filter(id__in=card_ids).update(deck=deck)
        return deck

    class Meta:
        model = models.Deck
        fields = ['id', 'name', 'is_active', 'url', 'planner_url', 'cards', 'card_ids', 'card_count']

class DeckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deck
        fields = ['name', 'is_active']

class DeckImportSerializer(serializers.Serializer):
    collection = serializers.SlugRelatedField(slug_field='id', queryset=models.Collection.objects.all())
    name = serializers.CharField(max_length=256)
    deck_list = serializers.CharField(style={'base_template': 'textarea.html'})

    def validate_name(self, value):
        if models.Deck.objects.filter(name=value).count() > 0:
            raise serializers.ValidationError('Deck (%s) already exists.' % value)
        return value

    def validate_deck_list(self, value):
        self.cards = list()
        self.cards, errors = deck_utils.validate_decklist(value.splitlines())

        if errors:
            raise serializers.ValidationError(errors)
        return value

    def save(self):
        deck = models.Deck.objects.create(name=self.validated_data['name'])
        for card in self.cards:
            card.deck = deck
            card.save()


class DeckPlannerSerializer(serializers.Serializer):
    deck_list = serializers.CharField(style={'base_template': 'textarea.html'})

    def validate_deck_list(self, value):
        cards = list()
        cards, errors = deck_utils.validate_decklist(value.splitlines())

        if errors:
            raise serializers.ValidationError(errors)
        return cards

