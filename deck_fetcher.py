# vim: set fileencoding=utf-8
import re
import urllib2

from util import *

class Deck:
  def __init__(self, cards, url, name, reachable_ranks, last_update):
    """
    Args:
      cards: map {string -> int}
    """
    self.url = url
    self.name = name
    self.reachable_ranks = reachable_ranks
    self.last_update = last_update
    self.cards = cards

    num_cards = 0
    for card, num in self.cards.iteritems():
      num_cards += num
    if num_cards != 30:
      raise Exception('Invalid deck: ' + str(num_cards) + ' cards.\n' + str(self))

  def __str__(self):
    return (self.name
        + '\n  ' + self.url
        + '\n  ' + self.reachable_ranks
        + '\n  ' + self.last_update
        + '\n    '
        + '\n    '.join(
          [str(num) + ' ' + card for card, num in self.cards.iteritems()]))

@cache_result_in('decks.pickle')
def get_decks():
  decks = []
  for file_name in ICY_VEIN_DECK_FILE_NAMES:
    print 'Fetching from', file_name
    decks += _fetch_decks_from_icy_veins(file_name)
  decks.extend(TRUMP_DECKS)
  decks.extend(_fetch_decks_from_hearthpwn())
  return decks

################################################################################
# Trump decks
################################################################################

TRUMP_DECKS = [Deck(
  cards={
    'Mortal Coil': 1,
    'Power Overwhelming': 2,
    'Abusive Sergeant': 2,
    'Flame Imp': 2,
    'Voidwalker': 2,
    'Dire Wolf Alpha': 2,
    'Haunted Creeper': 2,
    'Ironbeak Owl': 1,
    'Knife Juggler': 2,
    'Nerubian Egg': 2,
    'Imp Gang Boss': 2,
    'Void Terror': 1,
    'Imp-losion': 2,
    'Dark Iron Dwarf': 1,
    'Defender of Argus': 2,
    'Voidcaller': 2,
    'Doomguard': 2},
   url='https://www.youtube.com/watch?v=DBjJ_H3GDNk',
   name='Trump\'s Zoo',
   reachable_ranks='-',
   last_update='2015-07-11')]

################################################################################
# Icy Veins decks
################################################################################

ICY_VEIN_DECK_FILE_NAMES = [
  'decks/druid_decks.txt',
  'decks/hunter_decks.txt',
  'decks/mage_decks.txt',
  'decks/paladin_decks.txt',
  'decks/priest_decks.txt',
  'decks/rogue_decks.txt',
  'decks/shaman_decks.txt',
  'decks/warlock_decks.txt',
  'decks/warrior_decks.txt',
]

def _fetch_decks_from_icy_veins(file_name):
  unfetched_decks = []
  with open(file_name) as f:
    for line in f:
      m = re.search('<a href="(http://[^"]*)">([^<]*)</a>', line)
      if m:
        deck = {}
        deck['url'] = m.group(1)
        deck['name'] = m.group(2)
        continue
      m = re.search('<td class="deck_presentation_rank">([^<]*)</td>', line)
      if m:
        deck['reachable_ranks'] = m.group(1)
        continue
      m = re.search('<td class="deck_presentation_last_update">([^<]*)</td>',
          line)
      if m:
        deck['last_update'] = m.group(1)
        unfetched_decks.append(deck)

  decks = [Deck(_fetch_cards_from_icy_vein(d['url']), **d)
           for d in unfetched_decks]
  return decks


def _fetch_cards_from_icy_vein(url):
  cards = {}
  response = urllib2.urlopen(url)
  html = response.read()
  for line in html.splitlines():
    m = re.search(
        '<li>(\d)x\s+<a class="hearthstone_tooltip_link q\d" [^>]*>([^<]*)' +
        '</a>(\s*<span class="expansion_marker">[^<]*</span>)?</li>$',
        line)
    if m:
      name = m.group(2)
      number = int(m.group(1))
      cards[name] = number

  return cards

################################################################################
# Hearthpwn decks
################################################################################

def _fetch_decks_from_hearthpwn():
  unfetched_urls = set([])
  unfetched_decks = []
  for url in ['http://www.hearthpwn.com/decks?sort=-viewcount',
              'http://www.hearthpwn.com/decks?sort=-rating']:
    response = urllib2.urlopen(url)
    html = response.read()
    for line in html.splitlines():
      m = re.search('<a href="(/decks/[^"]*)">([^<]*)</a></span>$',
          line)
      if m:
        deck = {}
        deck['name'] = m.group(2).replace('&#x27;', '\'')
        deck['url'] = 'http://www.hearthpwn.com' + m.group(1)
        continue
      m = re.search('<abbr class="tip standard-date standard-datetime" [^>]*>([^<]*)</abbr>$',
                    line)
      if m:
        deck['last_update'] = m.group(1)
        deck['reachable_ranks'] = '--'
        if deck['url'] not in unfetched_urls:
          unfetched_urls.add(deck['url'])
          unfetched_decks.append(deck)
  decks = [Deck(_fetch_cards_from_hearthpwn(d['url']), **d)
           for d in unfetched_decks]
  print 'Fetched', len(decks), 'decks from hearthpwn'
  return decks

def _fetch_cards_from_hearthpwn(url):
  cards = {}
  response = urllib2.urlopen(url)
  html = response.read()
  for line in html.splitlines():
    m = re.search(
        '<b style="[^"]*"><a href="/cards/[^"]*" class="[^"]*">([^<]*)</a></b>$',
        line)
    if m:
      name = m.group(1).replace('&#x27;', '\'')
      continue
    m = re.match('× (\d*)', line)
    if m:
      number = int(m.group(1))
      cards[name] = number
  return cards
