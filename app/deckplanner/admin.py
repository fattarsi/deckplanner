from django.contrib import admin
from deckplanner import models


class CollectionAdmin(admin.ModelAdmin):
    pass

class DeckAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'rarity',  'deck']
    list_filter = ['deck', 'oracle_card__type_line', 'oracle_card__rarity']

    def rarity(self, obj):
        return obj.oracle_card.rarity

class OracleCardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'rarity', 'type_line', 'edhrec_rank']
    list_filter = ['rarity', 'set_code']

admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Deck, DeckAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.OracleCard, OracleCardAdmin)
