class BiciTransition:

    def __init__(self, index, amount, time, real):
        self.index = index
        self.amount = amount
        self.time = int(time)
        self.real = real
    def print(self):
        print(self.index)
