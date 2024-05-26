import csv

from django.core.management.base import BaseCommand, CommandError
from deckplanner import models


class Command(BaseCommand):
    help = "Import data from manabox csv"

    def add_arguments(self, parser):
        parser.add_argument("manabox_csv", type=str)

    def handle(self, *args, **options):
        c, _ = models.Collection.objects.get_or_create(name='default')
        self.stdout.write(self.style.SUCCESS(options))
        with open(options['manabox_csv'], newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                models.Card.objects.create(name=row[2], collection=c)

