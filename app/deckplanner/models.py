from django.db import models


class Collection(models.Model):
    name = models.CharField(max_length=256)

class Deck(models.Model):
    name = models.CharField(max_length=256)

class Card(models.Model):
    name = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, blank=True, null=True)

    set_code = models.CharField(max_length=256)
    set_name = models.CharField(max_length=256)
    rarity = models.CharField(max_length=256)
    collector_number = models.CharField(max_length=256)
    scryfall_id = models.CharField(max_length=256)
