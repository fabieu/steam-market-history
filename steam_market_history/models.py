from dataclasses import dataclass


@dataclass
class MarketTransaction:
    game_name: str | None
    item_name: str | None
    listed_date: str | None
    price: str | None
    gain_or_loss: str | None
    image_url: str | None
