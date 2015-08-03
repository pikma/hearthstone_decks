from deck_fetcher import get_decks, Deck
from all_cards import get_crafting_costs

# Map {string -> int}. Contains only the non-free cards.
COLLECTION = {
    'Abomination': 1,
    'Acolyte of Pain': 1,
    'Aldor Peacekeeper': 1,
    'Alexstrasza': 1,
    'Amani Berserker': 2,
    'Ancestor\'s Call': 1,
    'Ancient Watcher': 1,
    'Ancient of War': 1,
    'Annoy-o-Tron': 1,
    'Argent Protector': 1,
    'Azure Drake': 1,
    'Baron Rivendare': 1,
    'Battle Rage': 2,
    'Betrayal': 2,
    'Blade Flurry': 1,
    'Bloodsail Corsair': 1,
    'Bloodsail Raider': 2,
    'Circle of Healing': 1,
    'Cogmaster': 1,
    'Coldlight Oracle': 1,
    'Conceal': 1,
    'Cruel Taskmaster': 1,
    'Cult Master': 2,
    'Dancing Swords': 2,
    'Dark Iron Dwarf': 1,
    'Deathlord': 2,
    'Defias Ringleader': 1,
    'Doomguard': 2,
    'Druid of the Fang': 1,
    'Eaglehorn Bow': 1,
    'Emperor Cobra': 1,
    'Eviscerate': 1,
    'Explosive Sheep': 1,
    'Faerie Dragon': 2,
    'Fen Creeper': 1,
    'Flame Imp': 1,
    'Flesheating Ghoul': 1,
    'Forked Lightning': 1,
    'Freezing Trap': 1,
    'Frost Elemental': 2,
    'Glaivezooka': 2,
    'Grommash Hellscream': 1,
    'Harvest Golem': 1,
    'Haunted Creeper': 2,
    'Holy Fire': 1,
    'Ice Barrier': 1,
    'Inner Fire': 2,
    'Iron Sensei': 1,
    'Ironbeak Owl': 1,
    'Keeper of the Grove': 1,
    'Lightspawn': 2,
    'Loatheb': 1,
    'Maexxna': 1,
    'Mana Wraith': 1,
    'Mana Wyrm': 1,
    'Mechanical Yeti': 1,
    'Metaltooth Leaper': 1,
    'Misdirection': 1,
    'Mogu\'shan Warden': 2,
    'Naturalize': 2,
    'Nerub\'ar Weblord': 2,
    'Nerubian Egg': 2,
    'Noble Sacrifice': 1,
    'Power Overwhelming': 1,
    'Power of the Wild': 1,
    'Preparation': 1,
    'Puddlestomper': 2,
    'Raging Worgen': 2,
    'Scarlet Crusader': 1,
    'Scavenging Hyena': 1,
    'Secretkeeper': 1,
    'Shadowstep': 1,
    'Shieldbearer': 1,
    'Siege Engine': 1,
    'Silence': 2,
    'Sludge Belcher': 2,
    'Spectral Knight': 2,
    'Spellbender': 1,
    'Spellbreaker': 1,
    'Spider Tank': 2,
    'Stampeding Kodo': 1,
    'Stoneskin Gargoyle': 2,
    'Stormforged Axe': 2,
    'Summoning Portal': 1,
    'Sunwalker': 2,
    'Tauren Warrior': 2,
    'Temple Enforcer': 1,
    'Twisting Nether': 1,
    'Unstable Ghoul': 2,
    'Windfury': 2,
    'Wisp': 1,
    'Worgen Infiltrator': 2,
    'Wrath': 1,
    'Young Dragonhawk': 1,
    'Young Priestess': 1,
    'Youthful Brewmaster': 1,
}

_CRAFTING_COSTS = get_crafting_costs()
print 'Got ' + str(len(_CRAFTING_COSTS)) + ' cards'
def crafting_cost(card, collection):
  if card == 'Old Murk-Eye':
    return deck_cost({
        'Murloc Raider': 1,
        'Bluegill Warrior': 1,
        'Grimscale Oracle': 1,
        'Murloc Tidehunter': 1,
        'Coldlight Oracle': 1,
        'Coldlight Seer': 1,
        'Murloc Tidecaller': 1,
        'Murloc Warleader': 1,
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
    cost = crafting_cost(card, collection)
    if cost == 0:
      s += ' (-)'
    else:
      num_missing = max(0, num - collection.get(card, 0))
      s += ' (' + str(num_missing) + ' * ' + str(cost) + ')'
    cards_str.append(s)

  return (deck.name
      + '\n  ' + deck.url
      + '\n  ' + deck.reachable_ranks
      + '\n  ' + deck.last_update
      + ''.join(
        ['\n    ' + card_str for card_str in cards_str]))

decks = get_decks()
print 'Got ' + str(len(decks)) + ' decks\n'

# Validate collection.
for card, num in COLLECTION.iteritems():
  if card != 'Old Murk-Eye' and card not in _CRAFTING_COSTS:
    raise Exception('Invalid card in collection: \'' + str(card) + '\'')

# Show cards that can be disanchanted
print 'Useless cards:'
total_disenchant_gain = 0
for card, num in COLLECTION.iteritems():
  max_num_in_decks = 0
  for deck in decks:
    max_num_in_decks = max(max_num_in_decks, deck.cards.get(card, 0))
  num_unused = num - max_num_in_decks
  cost = crafting_cost(card, {})
  DISENCHANT_GAINS = {0: 0, 40: 5, 100: 20, 400: 100, 1600: 400}
  if card == 'Old Murk-Eye':
    disenchant_gain = 0
  else:
    disenchant_gain = DISENCHANT_GAINS[cost]
  if disenchant_gain == 400:
    # Never disenchant legendaries.
    continue
  if num_unused > 0 and disenchant_gain > 0:
    total_disenchant_gain += disenchant_gain * num_unused
    print '  ' + card + ' (' + str(num_unused) + ' * ' + str(disenchant_gain) + ')'
print 'Total: ' + str(total_disenchant_gain) + ' dust \n'


sorted_decks = sorted(decks, key=lambda d : deck_cost(d.cards, COLLECTION))
for deck in sorted_decks:
  if deck.name == 'Basic':
    continue
  print ('\nCost: ' + str(deck_cost(deck.cards, COLLECTION)) +
         ' (/' + str(deck_cost(deck.cards, {})) + ')')
  print print_deck(deck, COLLECTION)
