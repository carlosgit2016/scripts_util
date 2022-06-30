from collections import Counter

def shoes_store():
    x = int(input())
    shoes = list(map(int, input().split()))

    counter_shoes = Counter(shoes)
    c = int(input())

    price = 0
    for _ in range(c):
        s, value = map(int, input().split())
        if counter_shoes.get(s) is not None and counter_shoes.get(s) > 0:
            price += value
            counter_shoes.subtract((s,))
    print(price)    

if __name__ == "__main__":
    shoes_store()
