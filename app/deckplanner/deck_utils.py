from deckplanner import models


BASIC_LANDS = ('Plains', 'Island', 'Swamp', 'Mountain', 'Forest')

def validate_decklist(decklist):
        errors = list()
        cards = list()
        for line in decklist:
            line = line.strip()

            # Do not include anything below the sideboard
            if line.startswith('// SIDEBOARD'):
                break

            if line.startswith('//') or not line:
                continue

            number, rest = line.split(' ', 1)
            number = int(number)
            name = rest.split(' (', 1)[0]

            # Skip any basic lands
            if name in BASIC_LANDS:
                continue

            available = models.Card.objects.filter(name=name).filter(deck=None)
            if available.count() < number:
                in_decks = models.Card.objects.filter(name=name).filter(deck__isnull=False).values_list('deck__name', flat=True)
                errors.append('Not available: %s  Need: %s, In decks: %s' % (name, number, ' | '.join(in_decks)))
                continue
            available_cards = list(available)
            for _ in range(number):
                cards.append(available_cards.pop())
        return (cards, errors)
