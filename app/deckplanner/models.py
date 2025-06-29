from django.db import models


class OracleCard(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    mana_cost = models.CharField(max_length=256)
    cmc = models.CharField(max_length=256)
    type_line = models.CharField(max_length=256)
    oracle_text = models.CharField(max_length=4096)
    power = models.CharField(max_length=256)
    rarity = models.CharField(max_length=256)
    collector_number = models.CharField(max_length=256)
    toughness = models.CharField(max_length=256)
    edhrec_rank = models.IntegerField()
    color_identity = models.JSONField(default=list)
    set_code = models.CharField(max_length=256)
    set_name = models.CharField(max_length=256)
    prices = models.JSONField(default=dict)
    image_uris = models.JSONField(default=dict)
    game_changer = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=256)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.SET_NULL, blank=True, null=True, related_name='cards')
    oracle_card = models.ForeignKey(OracleCard, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
