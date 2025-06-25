from deckplanner import models


BASIC_LANDS = ('Plains', 'Island', 'Swamp', 'Mountain', 'Forest')


def get_color_identity(cards):
    # Use a set so we only keep unique color identity letters
    all_colors = set()

    for card in cards:
        # color_identity is a comma-separated string like "B,U,R"
        color_identity = card.oracle_card.color_identity
        if color_identity:
            all_colors.update(color_identity)

    # Sort them in some standard order (WUBRG is common in Magic)
    color_order = ['W', 'U', 'B', 'R', 'G']
    sorted_colors = [c for c in color_order if c in all_colors]

    return sorted_colors


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
