def minion_game(string):
    # your code goes here
    # Stuart = consonants
    # Kevin = vowel AEIOU
    b = [string[_] for _ in range(len(string))]
    
    kevin_score = 0
    stuart_score = 0
    S_size = len(b)
    
    for i in range(1, S_size+1): # 1, 2, 3, 4, 5, 6
        for j in range(S_size-(i-1)): # 0, 1, 2, 3, 4, 5

            sub = "".join(b[j:i+j])
            is_vowel = sub.startswith(('A', 'E', 'I', 'O', 'U'))
            if is_vowel:
                kevin_score+=1
            else:
                stuart_score+=1
            
    if kevin_score > stuart_score:
        print('Kevin', kevin_score)
    elif stuart_score > kevin_score:
        print('Stuart', stuart_score)
    else:
        print('Draw')