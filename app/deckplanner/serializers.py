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
    collection = CollectionSerializer()
    name = serializers.CharField(max_length=256)
    deck_list = serializers.CharField(style={'base_template': 'textarea.html'})