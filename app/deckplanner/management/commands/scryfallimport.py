import ijson
from django.core.management.base import BaseCommand, CommandError
from deckplanner import models

class Command(BaseCommand):
    help = 'Imports OracleCard data from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to be imported.')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        models.OracleCard.objects.all().delete()
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                objects = ijson.items(file, 'item')
                for data in objects:
                    self.create_oracle_card(data)
        except FileNotFoundError:
            raise CommandError(f'The file {json_file} does not exist.')
        except ijson.JSONError:
            raise CommandError(f'The file {json_file} is not valid JSON.')

        self.stdout.write(self.style.SUCCESS('Successfully imported cards.'))

    def create_oracle_card(self, data):
        try:
            models.OracleCard.objects.create(
                id=data['id'],
                name=data.get('name', ''),
                mana_cost=data.get('mana_cost', ''),
                cmc=str(data.get('cmc', '')),
                type_line=data.get('type_line', ''),
                oracle_text=data.get('oracle_text', ''),
                power=data.get('power', ''),
                rarity=data.get('rarity', ''),
                toughness=data.get('toughness', ''),
                edhrec_rank=data.get('edhrec_rank', 0),
                color_identity=",".join(data.get('color_identity', [])),
                set_code=data.get('set', ''),
                set_name=data.get('set_name', '')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating card: {e}'))
