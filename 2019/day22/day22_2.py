class Deck:
    def __init__(self, N=10007):
        self.N = N
        self.a = 1
        self.b = 0
        # x = (a * x + b) % N

    def deal_into_new_stack(self):
        # (-x - 1) % N
        # (-(a x + b) -1) % N
        # (-a x - b - 1) % N
        self.a, self.b = - self.a, - self.b - 1

    def cut(self, n):
        # (x + n) % N
        # ((a x + b) + n) % N
        # (a x + b + n) % N
        self.b += n
    
    def deal_with_increment(self, n):
        # (-x * n) % N
        # (-(a x + b) * n) % N
        # (- a n x - b n) % N
        self.a, self.b = - self.a * n, - self.b * n

    def step(self, cmd):
        if cmd == 'deal into new stack':
            self.deal_into_new_stack()
        elif cmd.startswith('deal with increment'):
            N = int(cmd.rsplit(' ', 1)[1])
            self.deal_with_increment(N)
        elif cmd.startswith('cut'):
            N = int(cmd.rsplit(' ', 1)[1])
            self.cut(N)

