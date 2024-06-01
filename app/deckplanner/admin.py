from django.contrib import admin
from deckplanner import models


class CollectionAdmin(admin.ModelAdmin):
    pass

class DeckAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'set_code', 'set_name', 'rarity', 'deck']
    list_filter = ['deck', 'rarity', 'set_name']

class OracleCardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'rarity', 'type_line', 'edhrec_rank']
    list_filter = ['rarity', 'set_code']

admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Deck, DeckAdmin)
admin.site.register(models.Card, CardAdmin)
admin.site.register(models.OracleCard, OracleCardAdmin)