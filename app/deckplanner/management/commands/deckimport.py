import os
from django.core.management.base import BaseCommand, CommandError
from deckplanner import models, deck_utils


class Command(BaseCommand):
    help = 'Import decks from a directory'

    def add_arguments(self, parser):
        parser.add_argument(
            'directory',
            type=str,
            help='The path to the directory containing decks to import.'
        )

    def handle(self, *args, **options):
        self.stdout.write(f"Removing previous decks.")
        models.Deck.objects.all().delete()
        directory = options['directory']

        if not os.path.isdir(directory):
            raise CommandError(f"'{directory}' is not a valid directory.")

        self.stdout.write(f"Scanning directory: {directory}")

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                self.stdout.write(f"Importing: {filename}")
                try:
                    self.validate_file(filepath)
                except Exception as e:
                    self.stderr.write(f"Error importing {filename}: {e}")
            else:
                self.stdout.write(f"Skipping non-file: {filename}")

    def validate_file(self, filepath):
        with open(filepath) as f:
            cards, errors = deck_utils.validate_decklist(f)


        if errors:
            self.stderr.write(f"Errors during import: {errors}")
        deck = models.Deck.objects.create(name=os.path.basename(filepath))
        for card in cards:
            card.deck = deck
            card.save()
