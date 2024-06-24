= Deckplanner =

Deckplanner helps you plan decks so that you can see if cards are available from your collection (or currently used in other decks).

== Setup ==

* make the project
```
make
```

* Run the project
```
make run
```

* Import the oracle cards

    * Download the oracle card data from scryfall.com
    * Use the management command to import
```
python manage.py scryfallimport <json file>
```


* Import collection from manabox

    * Export collection from manabox
    * Use the management command to import
```
python manage.py manaboximport <csv file>
```

