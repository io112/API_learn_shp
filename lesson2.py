import math

class Pig:
    color = "pink"

    def __init__(self, name):
        self.pig_name = name
        self.health = 10
        self.h = 1
        self.food = 0

    def __add__(self, other):
        return self.health + other.health

    def heal(self, health):
        self.health += health

    def eat(self):
        self.food += 1


def test(name):
    peppa = Pig(name)
    peppa.eat()
    peppa.heal(5)
    my_list = (1, 3, 6, 8, 54)
    for i in range(len(my_list)):
        print(i)
    return peppa.pig_name


def main():
    a = Pig('1')
    b = Pig('2')
    a.health = 5
    print(a + b)


if __name__ == '__main__':
    main()
