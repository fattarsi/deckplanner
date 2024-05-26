from django.contrib import admin
from deckplanner import models


class CollectionAdmin(admin.ModelAdmin):
    pass

class DeckAdmin(admin.ModelAdmin):
    pass

class CardAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Collection, CollectionAdmin)
admin.site.register(models.Deck, DeckAdmin)
admin.site.register(models.Card, CardAdmin)