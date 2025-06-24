#!/bin/bash
python manage.py scryfallimport ../default-cards-20250623091546.json
python manage.py manaboximport ../ManaBox_Collection.csv --excludeLists Owen Wishlist 'Battle of the Pelennor Fields Scene [Set of 18]' 'Vintage Power Cube'
python manage.py deckimport ../active_decks/
