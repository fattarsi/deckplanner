from collections import namedtuple

from rest_framework import serializers

from deckplanner import models, deck_utils


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['name']

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deck
        fields = ['name', 'is_active']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ['name']

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
