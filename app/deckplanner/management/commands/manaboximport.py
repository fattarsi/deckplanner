import csv

from django.core.management.base import BaseCommand, CommandError
from deckplanner import models


class Command(BaseCommand):
    help = "Import data from manabox csv"

    def add_arguments(self, parser):
        parser.add_argument("manabox_csv", type=str)
        parser.add_argument(
            "--excludeLists",
            nargs='+',
            type=str,
            default=[],
            help="Names of lists to exclude when the list is of type 'list' (e.g. Wishlist)."
        )

    def handle(self, *args, **options):
        excluded_lists = options['excludeLists']
        self.stdout.write(self.style.SUCCESS(f"Excluding lists: {excluded_lists}"))
        c, _ = models.Collection.objects.get_or_create(name='default')
        models.Card.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(options))
        with open(options['manabox_csv'], newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) # skip headers
            for row in reader:
                list_name = row[0]
                list_type = row[1]
                # Only process if it's not an excluded list
                if list_type == "list" and list_name in excluded_lists:
                    self.stdout.write(
                        f"Skipping list '{list_name}' because it's excluded"
                    )
                    continue
                name = row[2]
                quantity = int(row[8])
                scryfall_id = row[10]
                try:
                    oc = models.OracleCard.objects.get(id=scryfall_id)
                except models.OracleCard.DoesNotExist:
                    self.stdout.write('%s not found by UUID' % name)
                    oc = models.OracleCard.objects.filter(name=name).first()
                for _ in range(quantity):
                    models.Card.objects.create(
                        collection=c,
                        name=name,
                        oracle_card=oc
                    )

