from collections import defaultdict

n,m = map(int, input().split())
d = defaultdict(list) 

for x in range(int(n) + int(m)):
    if(x < int(n)):
        d[input()].append(x + 1)
    else:
        b = input()
        if b in d:
            print(' '.join(map(str,d[b])))
        else:
            print(-1)
