from deck_fetcher import get_decks, Deck
from all_cards import get_crafting_costs


# My collection of cards. It only contains the non-free cards.
COLLECTION = {
    'Abomination': 0,
    'Abusive Sergeant': 2,
    'Acolyte of Pain': 2,
    'Aldor Peacekeeper': 2,
    'Alexstrasza': 1,
    'Amani Berserker': 2,
    'Ancestor\'s Call': 1,
    'Ancient Watcher': 1,
    'Ancient of War': 1,
    'Annoy-o-Tron': 1,
    'Arathi Weaponsmith': 1,
    'Argent Protector': 2,
    'Argent Squire': 2,
    'Azure Drake': 1,
    'Bane of Doom': 1,
    'Baron Rivendare': 1,
    'Battle Rage': 2,
    'Betrayal': 0,
    'Blade Flurry': 1,
    'Blizzard': 1,
    'Bloodsail Corsair': 1,
    'Bloodsail Raider': 2,
    'Circle of Healing': 2,
    'Cogmaster': 1,
    'Coldlight Oracle': 1,
    'Coldlight Seer': 1,
    'Conceal': 1,
    'Counterspell': 1,
    'Cruel Taskmaster': 2,
    'Cult Master': 0,
    'Dancing Swords': 2,
    'Dark Iron Dwarf': 2,
    'Deathlord': 2,
    'Defender of Argus': 2,
    'Defias Ringleader': 1,
    'Demonfire': 1,
    'Dire Wolf Alpha': 2,
    'Doomguard': 2,
    'Druid of the Claw': 2,
    'Druid of the Fang': 0,
    'Eaglehorn Bow': 1,
    'Earthen Ring Farseer': 1,
    'Emperor Cobra': 1,
    'Eviscerate': 2,
    'Explosive Sheep': 1,
    'Explosive Trap': 2,
    'Eye for an Eye': 1,
    'Faerie Dragon': 2,
    'Fen Creeper': 1,
    'Feugen': 1,
    'Flame Imp': 2,
    'Flesheating Ghoul': 0,
    'Forked Lightning': 0,
    'Freezing Trap': 1,
    'Frost Elemental': 0,
    'Gladiator\'s Longbow': 1,
    'Glaivezooka': 2,
    'Grommash Hellscream': 1,
    'Harvest Golem': 2,
    'Haunted Creeper': 2,
    'Holy Fire': 1,
    'Holy Wrath': 1,
    'Ice Barrier': 1,
    'Ice Lance': 2,
    'Injured Blademaster': 2,
    'Inner Fire': 2,
    'Iron Sensei': 0,
    'Ironbeak Owl': 2,
    'Keeper of the Grove': 1,
    'Kidnapper': 1,
    'Knife Juggler': 2,
    'Lava Burst': 1,
    'Leper Gnome': 2,
    'Lightspawn': 0,
    'Loatheb': 1,
    'Mad Bomber': 1,
    'Mad Scientist': 2,
    'Maexxna': 1,
    'Mark of Nature': 1,
    'Mana Wraith': 1,
    'Mana Wyrm': 1,
    'Mark of Nature': 1,
    'Mechanical Yeti': 1,
    'Metaltooth Leaper': 0,
    'Mind Control Tech': 1,
    'Misdirection': 1,
    'Mogu\'shan Warden': 0,
    'Naturalize': 2,
    'Nerub\'ar Weblord': 2,
    'Nerubian Egg': 2,
    'Noble Sacrifice': 0,
    'Patient Assassin': 2,
    'Pint-Sized Summoner': 2,
    'Power Overwhelming': 1,
    'Power of the Wild': 2,
    'Preparation': 1,
    'Priestess of Elune': 1,
    'Puddlestomper': 1,
    'Raging Worgen': 2,
    'Savannah Highmane': 1,
    'Scarlet Crusader': 1,
    'Scavenging Hyena': 2,
    'Secretkeeper': 1,
    'Shadowstep': 1,
    'Shieldbearer': 2,
    'Siege Engine': 0,
    'Silence': 0,
    'Silvermoon Guardian': 1,
    'Siphon Soul': 1,
    'Slam': 2,
    'Sludge Belcher': 2,
    'Soul of the Forest': 1,
    'Southsea Deckhand': 1,
    'Spectral Knight': 2,
    'Spellbender': 0,
    'Spellbreaker': 1,
    'Spider Tank': 2,
    'Stalagg': 1,
    'Stampeding Kodo': 1,
    'Stoneskin Gargoyle': 2,
    'Stormforged Axe': 2,
    'Summoning Portal': 2,
    'Sunwalker': 2,
    'Tauren Warrior': 0,
    'Temple Enforcer': 1,
    'Thoughtsteal': 1,
    'Thrallmar Farseer': 1,
    'Twisting Nether': 0,
    'Unstable Ghoul': 2,
    'Venture Co. Mercenary': 1,
    'Wailing Soul': 2,
    'Windfury': 2,
    'Windfury Harpy': 1,
    'Wisp': 2,
    'Worgen Infiltrator': 2,
    'Wrath': 1,
    'Young Dragonhawk': 0,
    'Young Priestess': 2,
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
