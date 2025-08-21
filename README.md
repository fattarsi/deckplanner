# Deckplanner

Deckplanner helps you plan Magic: The Gathering decks by checking card availability in your collection (or whether they’re already in other decks).

---

## Setup

### Build the project
```bash
make
```

### Run the project
```bash
make run
```

### Import Oracle cards
1. Download the **Oracle card data** from [Scryfall Bulk Data](https://scryfall.com/docs/api/bulk-data).
2. Import the data:
   ```bash
   python manage.py scryfallimport <json_file>
   ```
   - Re-running this command is **idempotent** (safe to run multiple times).

### Import collection from ManaBox
1. Export your collection from the **ManaBox mobile app**.
2. Import the collection:
   ```bash
   python manage.py manaboximport <csv_file>
   ```
   - ⚠️ Re-running this will **delete all cards** before importing.

---

## Useful Commands

### Run management commands inside Docker
```bash
docker exec -it deckplanner_backend /bin/bash
cd app/app/
```

### Import ManaBox collection (excluding lists)
```bash
python manage.py manaboximport ../ManaBox_Collection.csv \
  --excludeLists Owen Wishlist 'Battle of the Pelennor Fields Scene [Set of 18]' 'Vintage Power Cube'
```

### Import decks
```bash
python manage.py deckimport ../active_decks/
```

---

## Notes
- Deckplanner uses **Scryfall data** for Oracle cards.
- Collections are managed via **ManaBox exports**.

