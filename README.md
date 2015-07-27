To run it, you need a mashape key (the program uses a mashape API to fetch the
up-to-date list of cards and their rarities). Get one at www.mashape.com.

Then run the program like this:
```bash
MASHAPE_KEY="Insert Your Key Here" python deck.py
```

The first run will take some time (it fetches a bunch of decks from Icy Veins),
but the subsequent runs will be much faster. Change your card collection in
deck.py.
