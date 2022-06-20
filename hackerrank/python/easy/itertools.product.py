from itertools import product 

def run(A, B):

    p=list(product(A, B))
    for i in p:
        print(i, end=' ')


if __name__ == "__main__":
    A=list(map(int, input().split()))
    B=list(map(int, input().split()))
    run(A, B)
