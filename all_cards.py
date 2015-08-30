import unirest
import os

from util import *

CARD_SETS = [
  u'Classic',
  u'Naxxramas',
  u'Blackrock Mountain',
  u'Basic',
  u'Promotion',
  u'Goblins vs Gnomes',
  u'The Grand Tournament',
]

CRAFTING_COSTS = {
  u'Free': 0,
  u'Common': 40,
  u'Rare': 100,
  u'Epic': 400,
  u'Legendary': 1600,
}


@cache_result_in('cards.pickle')
def get_crafting_costs():
  """Returns a map{string -> int}, where the keys are the card names, and the
  values are the crafting costs."""
  api_key = os.environ['MASHAPE_KEY']
  response = unirest.get(
      "https://omgvamp-hearthstone-v1.p.mashape.com/cards?collectible=1",
      headers={"X-Mashape-Key": api_key}
      )
  cards = {}
  for card_set in CARD_SETS:
    for card in response.body[card_set]:
      name = str(card[u'name'])
      if card[u'cardSet'] == u'Basic':
        cards[name] = 0
      else:
        cards[name] = CRAFTING_COSTS[card[u'rarity']]

  return cards

