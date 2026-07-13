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
    def __init__(self, rank: str, suit: str) -> None:
        self.rank = rank
        self.suit = suit
        self.rank_index = RANKS.index(rank)
        self.suit_index = SUITS.index(suit)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return (
            self.rank_index == other.rank_index and self.suit_index == other.suit_index
        )

    def __lt__(self, other: "Card") -> bool:
        if self.rank_index == other.rank_index:
            return self.suit_index < other.suit_index
        return self.rank_index < other.rank_index

    def __gt__(self, other: "Card") -> bool:
        if self.rank_index == other.rank_index:
            return self.suit_index > other.suit_index
        return self.rank_index > other.rank_index

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Round:
    def resolve_round(self) -> int:
        raise NotImplementedError("Subclasses must implement resolve_round()")


# Don't touch above this line


class HighCardRound(Round):
    def __init__(self, card1: "Card", card2: "Card") -> None:
        super().__init__()
        self.card1 = card1
        self.card2 = card2

    def resolve_round(self) -> int:
        if self.card1 > self.card2:
            return 1
        if self.card1 < self.card2:
            return 2
        else:
            return 0


class LowCardRound(Round):
    def __init__(self, card1: "Card", card2: "Card") -> None:
        super().__init__()
        self.card1 = card1
        self.card2 = card2

    def resolve_round(self) -> int:
        if self.card1 > self.card2:
            return 2
        if self.card1 < self.card2:
            return 1
        else:
            return 0
