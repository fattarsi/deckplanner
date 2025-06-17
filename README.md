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

    * Download from https://scryfall.com/docs/api/bulk-data
    * Note: re-running this is idempotent


* Import collection from manabox

    * Export collection from manabox
    * Use the management command to import
```
python manage.py manaboximport <csv file>
```

    * Export data from the mobile app
    * Note: re-running this will delete all cards before importing.

== Useful Commands ==

* Run management commands
```
docker exec -it deckplanner_backend /bin/bash
cd app/app/
```
