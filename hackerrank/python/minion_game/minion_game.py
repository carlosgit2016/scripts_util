import time

def minion_game(string):
    t=time.time()
    start_with_vowels(string)
    print(t-time.time())

    t2=time.time()
    string.startswith(('A', 'I', 'O', 'E', 'U'))
    print(t2-time.time())

    print(t<t2)
    

def start_with_consoants(s):
    return not start_with_vowels(s)


def start_with_vowels(s) -> bool:
    f = s[0]
    return f in ('A', 'I', 'O', 'E', 'U')

if __name__ == '__main__':
    minion_game('BANANA')
