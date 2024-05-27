import csv

from django.core.management.base import BaseCommand, CommandError
from deckplanner import models


class Command(BaseCommand):
    help = "Import data from manabox csv"

    def add_arguments(self, parser):
        parser.add_argument("manabox_csv", type=str)

    def handle(self, *args, **options):
        c, _ = models.Collection.objects.get_or_create(name='default')
        models.Card.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(options))
        with open(options['manabox_csv'], newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) # skip headers
            for row in reader:
                name = row[2]
                set_code = row[3]
                set_name = row[4]
                collector_number = row[5]
                rarity = row[7]
                quantity = int(row[8])
                scryfall_id = row[10]
                for _ in range(quantity):
                    models.Card.objects.create(
                        collection=c,
                        name=name,
                        set_code=set_code,
                        set_name=set_name,
                        collector_number=collector_number,
                        rarity=rarity,
                        scryfall_id=scryfall_id
                    )

