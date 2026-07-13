SUITS: list[str] = ["Clubs", "Diamonds", "Hearts", "Spades"]

RANKS: list[str] = [
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
    "Ace",
]


class Card:
    rank: str
    suit: str
    rank_index: int
    suit_index: int

    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit
        self.rank_index = RANKS.index(rank)
        self.suit_index = SUITS.index(suit)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            raise ValueError("Need to be Card")

        if self.rank == other.rank and self.suit == other.suit:
            return True
        return False

    def __lt__(self, other: "Card") -> bool:
        if self.rank_index < other.rank_index:
            return True
        if self.rank_index == other.rank_index and self.suit_index < other.suit_index:
            return True
        return False

    def __gt__(self, other: "Card") -> bool:
        if self.rank_index > other.rank_index:
            return True
        if self.rank_index == other.rank_index and self.suit_index > other.suit_index:
            return True
        return False

    # don't touch below this line

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"
