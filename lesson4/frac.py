class Fraction:
    def __init__(self, x=0, y=1):
        self.x = x
        self.y = y

    def show(self):
        print(f'{self.x}/{self.y}')

    def __add__(self, other):
        self.x = self.x * other.y + other.x * self.y
        self.y *= other.y
        return self

    def read(self):
        self.x, self.y = map(int, input().split('/'))


def main():
    frac = Fraction()
    frac1 = Fraction()
    frac.read()
    frac1.read()
    frac = frac + frac1
    frac.show()


if __name__ == '__main__':
    main()
