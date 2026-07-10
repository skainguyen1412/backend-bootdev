import random

Card = tuple[str, str]


class DeckOfCards:
    SUITS: list[str] = ["Hearts", "Diamonds", "Clubs", "Spades"]
    RANKS: list[str] = [
        "Ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
    ]

    def __init__(self) -> None:
        self.__cards: list[Card] = []
        self.create_deck()

    def create_deck(self) -> None:
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.__cards.append((rank, suit))

    def shuffle_deck(self) -> None:
        random.shuffle(self.__cards)

    def deal_card(self) -> Card | None:
        if len(self.__cards) <= 0:
            return None

        return self.__cards.pop()

    # don't touch below this line

    def __str__(self) -> str:
        return f"The deck has {len(self.__cards)} cards"

