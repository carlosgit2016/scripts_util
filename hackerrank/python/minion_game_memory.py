from multiprocessing import Pool
import time

CALC_TIME=0

def calc_points(sub):
    """
        True = KEVIN
        False = Stuart
    """
    return sub.startswith(('A', 'E', 'I', 'O', 'U'))

def split_subs(i, string, size) -> list:
    subs = []
    for j in range(1, (size+1)-i):
        subs.append(string[i:j+i])
    return subs


def minion_game(string):
    size = len(string)
    p = Pool(processes=5)

    res = []
    matrix_subs = []
    for i in range(size): # size = 10000
        matrix_subs.extend(split_subs(i, string, size))

    kevin_score=0
    stuart_score=0
    calc_time = time.time()
    for s in matrix_subs:
        if calc_points(s):
            kevin_score+=1
        else:
            stuart_score+=1
    global CALC_TIME
    CALC_TIME=time.time() - calc_time
        
    if kevin_score > stuart_score:
        print('Kevin', kevin_score)
    elif stuart_score > kevin_score:
        print('Stuart', stuart_score)
    else:
        print('Draw')


if __name__ == "__main__":

    start_time = time.time()
    minion_game('BANANA'*600)
    print('MAIN TIME: ', (time.time() - start_time) - CALC_TIME)
    print('CALC TIME: ', CALC_TIME)
