def main():
    a = [1, 2, 5, 4]
    a.sort()


def ifcon():
    a, b = 1, 2
    a, b = b, a
    if a > b:
        print('a')
    elif not a == b:
        print('==')
    else:
        print('b')


def cycles():
    N = 10
    i = 0
    while i < N:
        print(i)
        i += 1


if __name__ == "__main__":
    main()
