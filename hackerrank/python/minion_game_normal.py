import time


KEVIN_SCORE=0
STUART_SCORE=0

def is_vowel(sub):
    """
        True = KEVIN
        False = Stuart
    """
    return sub[0] in ('A', 'E', 'I', 'O', 'U')

def minion_game(string):
    k_score=0
    stuart_score=0

    size = len(string)
    for i in range(size):
        if is_vowel(string[i]):
            k_score+=size-i
        else:
            stuart_score+=size-i

    if k_score > stuart_score:
        print('Kevin', k_score)
    elif stuart_score > k_score:
        print('Stuart', stuart_score)
    else:
        print('Draw')
      

if __name__ == "__main__":

    start_time = time.time()
    minion_game(input())
    print('MAIN TIME: ', (time.time() - start_time))
