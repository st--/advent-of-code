import numpy as np

class Deck:
    def __init__(self, num_cards=10007):
        self.deck = np.arange(num_cards)

    def deal_into_new_stack(self):
        self.deck = self.deck[::-1]

    def cut(self, N):
        if N > 0:
            self.deck = np.concatenate([self.deck[N:], self.deck[:N]])
        else:
            N = - N
            self.deck = np.concatenate([self.deck[-N:], self.deck[:-N]])

    def deal_with_increment(self, N):
        deck_size = len(self.deck)
        table = - np.ones(deck_size, int)
        pos = 0
        for i in range(deck_size):
            assert table[pos] == -1
            table[pos] = self.deck[i]
            pos += N
            if pos >= deck_size:
                pos -= deck_size
        assert not np.any(table == -1)
        self.deck = table
    
    def step(self, cmd):
        if cmd == 'deal into new stack':
            self.deal_into_new_stack()
        elif cmd.startswith('deal with increment'):
            N = int(cmd.rsplit(' ', 1)[1])
            self.deal_with_increment(N)
        elif cmd.startswith('cut'):
            N = int(cmd.rsplit(' ', 1)[1])
            self.cut(N)

deck = Deck()
for line in open("input.txt"):
    deck.step(line.strip())

print(np.argmax(deck.deck == 2019))
