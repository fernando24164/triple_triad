from src.card import Card


def drawn_card(card: Card) -> None:
    print(f" {'=' * 8} ")
    print(f"| {' ' * 4}{card.upper_number}  |")
    print(f"| {' ' * 3}{card.left_number} {card.right_number} |")
    print(f"| {' ' * 4}{card.bottom_number}  |")
    print(f"|{' ' * 8}|")
    print(f"|{' ' * 8}|")
    print(f" {'=' * 8} ")
