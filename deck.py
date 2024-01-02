import re
import json
from typing import List, Optional
from PIL import Image

CARDS_JSON_PATH: str = ""
# available_evos = ["skeletons", "knight", "firecracker", "mortar", "barbarians", "royal-recruits", "bats", "royal-giant", "archers"]

class Deck:
    """Clash Royale Deck Builder."""

    def __init__(self):
        """Init."""
        CARDS_JSON_PATH = "cards.json"
        with open(CARDS_JSON_PATH, encoding='utf-8') as file:
            self.cards = dict(json.load(file))["card_data"]
        self.card_w = 302
        self.card_h = 363
        self.card_ratio = self.card_w / self.card_h
        self.card_thumb_scale = 0.5
        self.card_thumb_w = int(self.card_w * self.card_thumb_scale)
        self.card_thumb_h = int(self.card_h * self.card_thumb_scale)
        
        self.available_evos = ["skeletons", "knight", "firecracker", "mortar", "barbarians", "royal-recruits", "bats", "royal-giant", "archers"]


    @property
    def valid_card_keys(self) -> List[str]:
        """Valid card keys."""
        return [card["key"] for card in self.cards]

    async def cards_json(self) -> List[dict]:
        """Load self._cards_json"""
        if self._cards_json is None:
            with open(CARDS_JSON_PATH) as f:
                self._cards_json = dict(json.load(f))["card_data"]
        return self._cards_json

    def card_id_to_key(self, card_id) -> Optional[str]:
        """Decklink id to card."""
        for card in self.cards:
            if card_id == str(card["id"]):
                return card["key"]
        return None

    def card_key_to_id(self, key) -> Optional[str]:
        """Card key to decklink id."""
        for card in self.cards:
            if key == card["key"]:
                return str(card["id"])
        return None

    def new_decklink_to_cards(self, url) -> Optional[List[str]]:
        """Convert decklink to cards."""
        card_keys = None
        m_crlink = re.search(
            r"(http|ftp|https)://link.clashroyale.com/(\w+)\?clashroyale://copyDeck\?deck=[\d;]+&slots=[\d;]+&id=\w+", url
        )
        if m_crlink:
            url = m_crlink.group()
            decklinks = re.findall(r"(\d+)", url)
            card_keys = []
            
            for decklink in decklinks:
                card_key = self.card_id_to_key(decklink)
                if card_key is not None:
                    card_keys.append(card_key)

        return card_keys
    
    def decklink_to_cards(self, url) -> Optional[List[str]]:
        """Convert decklink to cards."""
        card_keys = None
        m_crlink = re.search(
            r"(http|ftp|https)://link.clashroyale.com/deck/..\?deck=[\d\;]+", url
        )
        if m_crlink:
            url = m_crlink.group()
            decklinks = re.findall(r"2\d{7}", url)
            card_keys = []
            for decklink in decklinks:
                card_key = self.card_id_to_key(decklink)
                if card_key is not None:
                    card_keys.append(card_key)
        return card_keys

    def cards_to_decklink(self, cards):
        output = r"clashroyale://copyDeck?deck="
        output = r"https://link.clashroyale.com/deck/en?deck="
        card_keys = [self.card_key_to_id(card) for card in cards]
        card_keys = ";".join(card_keys)
        return output+card_keys

    async def decklink_url(self, deck_cards, war=False):
        """Decklink URL."""
        deck_cards = self.normalize_deck_data(deck_cards)
        ids = []
        for card in deck_cards:
            id = await self.card_key_to_id(card)
            if id is not None:
                ids.append(await self.card_key_to_id(card))
        url = "https://link.clashroyale.com/deck/en?deck=" + ";".join(ids)
        if war:
            url += "&war=1"
        return url


    def get_deck_elxir(self, card_keys):
        total_elixir = 0
        card_count = 0
        for card in self.cards:
            if card["key"] in card_keys:
                total_elixir += card["elixir"]
                if card["elixir"]:
                    card_count += 1
        average_elixir = "{:.3f}".format(total_elixir / card_count)
        return average_elixir


    def get_deck_image(self, deck):
        """Construct the deck with Pillow and return image."""
        card_w = 302
        card_h = 363
        card_x = 30
        card_y = 130
        size = (2476, 623)
        image = Image.new("RGBA", size)
        card_path = "assets/cards/"
        
        for i, card in enumerate(deck):
            if i==0 and card in self.available_evos:
                card_image_file = card_path + "{}-ev1.png".format(card)
            else:
                card_image_file = card_path +  "{}.png".format(card)
            card_image = Image.open(card_image_file).resize((card_w, card_h))
            box = (
                card_x + card_w * i,
                card_y,
                card_x + card_w * (i + 1),
                card_h + card_y,
            )
            try:
                image.paste(card_image, box, card_image)
            except ValueError:
                print(card_image_file)
        scale = 0.5
        scaled_size = tuple([x * scale for x in image.size])
        image.thumbnail(scaled_size)
        return image

    def create_deck_image_from_deck_link(self, deck_link):
        """Listen for decklinks, auto create useful image."""
        card_keys = self.decklink_to_cards(deck_link)
        if card_keys is None:
            card_keys = self.new_decklink_to_cards(deck_link)
            deck_image = self.get_deck_image(card_keys)
            if card_keys is None:
                        return  