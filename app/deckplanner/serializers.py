from collections import namedtuple

from rest_framework import serializers

from deckplanner import models


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['name']

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deck
        fields = ['name']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Card
        fields = ['name']

class DeckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deck
        fields = ['name']

class DeckImportSerializer(serializers.Serializer):
    collection = serializers.SlugRelatedField(slug_field='id', queryset=models.Collection.objects.all())
    name = serializers.CharField(max_length=256)
    deck_list = serializers.CharField(style={'base_template': 'textarea.html'})

    def validate_name(self, value):
        if models.Deck.objects.filter(name=value).count() > 0:
            raise serializers.ValidationError('Deck (%s) already exists.' % value)
        return value

    def validate_deck_list(self, value):
        errors = list()
        self.cards = list()
        for line in value.splitlines():
            if line.startswith('//') or not line:
                continue
            number, rest = line.split(' ', 1)
            number = int(number)
            name = rest.split(' (', 1)[0]
            available = models.Card.objects.filter(name=name).filter(deck=None)
            if available.count() < number:
                in_decks = models.Card.objects.filter(name=name).filter(deck__isnull=False).values_list('deck__name', flat=True)
                errors.append('Not available: %s  Need: %s, In decks: %s' % (name, number, ' | '.join(in_decks)))
                continue
            available_cards = list(available)
            for _ in range(number):
                self.cards.append(available_cards.pop())
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def save(self):
        deck = models.Deck.objects.create(name=self.validated_data['name'])
        for card in self.cards:
            card.deck = deck
            card.save()