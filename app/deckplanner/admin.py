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


admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Deck, DeckAdmin)
admin.site.register(models.Card, CardAdmin)