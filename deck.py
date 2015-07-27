from deck_fetcher import get_decks, Deck
from all_cards import get_crafting_costs

# Map {string -> int}. Contains only the non-free cards.
COLLECTION = {
    'Windfury': 2,
    'Frost Elemental': 2,
    'Temple Enforcer': 1,
    'Druid of the Fang': 1,
    'Fen Creeper': 1,
    'Cult Master': 1,
    'Dark Iron Dwarf': 1,
    'Lightspawn': 2,
    'Mechanical Yeti': 1,
    'Mogu\'shan Warden': 1,
    'Spellbreaker': 1,
    'Summoning Portal': 1,
    'Ice Barrier': 1,
    'Acolyte of Pain': 1,
    'Flesheating Ghoul': 1,
    'Harvest Golem': 1,
    'Raging Worgen': 2,
    'Scarlet Crusader': 1,
    'Spider Tank': 2,
    'Tauren Warrior': 2,
    'Glaivezooka': 2,
    'Stormforged Axe': 2,
    'Battle Rage': 1,
    'Betrayal': 1,
    'Eviscerate': 1,
    'Freezing Trap': 1,
    'Power of the Wild': 1,
    'Wrath': 1,
    'Amani Berserker': 2,
    'Annoy-o-Tron': 1,
    'Cruel Taskmaster': 1,
    'Defias Ringleader': 1,
    'Explosive Sheep': 1,
    'Faerie Dragon': 2,
    'Haunted Creeper': 2,
    'Ironbeak Owl': 1,
    'Nerub\'ar Weblord': 2,
    'Puddlestomper': 2,
    'Scavenging Hyena': 1,
    'Conceal': 1,
    'Forked Lightning': 1,
    'Inner Fire': 2,
    'Naturalize': 2,
    'Noble Sacrifice': 1,
    'Power Overwhelming': 1,
    'Cogmaster': 1,
    'Mana Wyrm': 1,
    'Shieldbearer': 1,
    'Worgen Infiltrator': 2,
    'Young Dragonhawk': 1,
    'Circle of Healing': 1,
    'Silence': 2,
    'Wisp': 1,
    'Holy Fire': 1,
    'Sunwalker': 2,
    'Abomination': 1,
    'Azure Drake': 1,
    'Doomguard': 2,
    'Siege Engine': 1,
    'Stampeding Kodo': 1,
    'Keeper of the Grove': 1,
    'Eaglehorn Bow': 1,
    'Coldlight Oracle': 1,
    'Emperor Cobra': 1,
    'Iron Sensei': 1,
    'Metaltooth Leaper': 1,
    'Blade Flurry': 1,
    'Misdirection': 1,
    'Ancient Watcher': 1,
    'Mana Wraith': 1,
    'Nerubian Egg': 2,
    'Secretkeeper': 1,
    'Twisting Nether': 1,
    'Ancient of War': 1,
    'Ancestor\'s Call': 1,
    'Spellbender': 1,
    'Alexstrasza': 1,
    'Grommash Hellscream': 1,
    'Maexxna': 1,
}

_CRAFTING_COSTS = get_crafting_costs()
print 'Got ' + str(len(_CRAFTING_COSTS)) + ' cards'
def crafting_cost(card, collection):
  if card == 'Old Murk-Eye':
    return deck_cost({
        'Murloc Raider': 1,
        'Bluegill Warrior': 1,
        'Grimscale Oracle': 1,
        'Murloc Tidehunter': 1
      }, collection)
  return _CRAFTING_COSTS[card]



def deck_cost(deck_cards, collection):
  cost = 0
  for card, number in deck_cards.iteritems():
    number_to_craft = number - collection.get(card, 0)
    if number_to_craft > 0:
      cost += number_to_craft * crafting_cost(card, collection)
  return cost

def print_deck(deck, collection):
  cards_str = []
  for card, num in deck.cards.iteritems():
    s = str(num) + ' ' + card
    num_in_collection = min(collection.get(card, 0), num)
    if num_in_collection > 0:
      s += ' (' + str(num_in_collection) + '/' + str(num) + ')'
    cards_str.append(s)

  return (deck.name
      + '\n  ' + deck.url
      + '\n  ' + deck.reachable_ranks
      + '\n  ' + deck.last_update
      + ''.join(
        ['\n    ' + card_str for card_str in cards_str]))

decks = get_decks()
print 'Got ' + str(len(decks)) + ' decks'

# Validate collection.
for card, num in COLLECTION.iteritems():
  if card != 'Old Murk-Eye' and card not in _CRAFTING_COSTS:
    raise 'Invalid card in collection: \'' + str(card) + '\''

sorted_decks = sorted(decks, key=lambda d : deck_cost(d.cards, COLLECTION))
# i = 0
for deck in sorted_decks:
  if deck.name == 'Basic':
    continue
  print '\nCost:', deck_cost(deck.cards, COLLECTION)
  print print_deck(deck, COLLECTION)
  # i += 1
  # if i == 20:
    # break
