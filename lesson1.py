import math


def main():
    n = int(input())
    count = 0
    count1 = 0
    for i in range(0, n - 1):
        a = int(input())
        count += a

    for i in range(1, n + 1):
        count1 += i
    print(count1 - count)


if __name__ == "__main__":
    main()