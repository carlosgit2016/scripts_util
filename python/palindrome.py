import re

def length_word(w):
    # pattern, repl, string
    w = re.sub(r'\s*', '', w)
    word_length = len(w)
    if (word_length % 2 == 0):
        return False
    else:
        f = w[0:word_length//2]
        s = w[word_length//2 + 1:word_length]

        new_s = []
        for letter in range(len(s) -1, -1, -1):
            new_s.append(s[letter])
            
        return f == ''.join(new_s)

def stack_palindrome(w):
    w = re.sub(r'\s*', '', w)
    stack = []
    for letter in w:
        stack.append(letter)
    reverse_word = ''
    for letter in range(len(w)):
        reverse_word += stack.pop()

    return w == reverse_word

def test_length_word():
    palindromes = [
        {'is': True,'p': 'arara'},
        {'is': True,'p': 'rodador'},
        {'is': True,'p': 'ana'},
        {'is': False,'p': 'carlos'},
        {'is': False,'p': 'maria'},
        {'is': True,'p': 'ame o poema'}
    ]

    for p in palindromes:
        print('word:', p['p'])
        print('expected:', p['is'])
        assert p['is'] == length_word(p['p'])

def test_stack_palindrome():
    palindromes = [
        {'is': True,'p': 'arara'},
        {'is': True,'p': 'rodador'},
        {'is': True,'p': 'ana'},
        {'is': False,'p': 'carlos'},
        {'is': False,'p': 'maria'},
        {'is': True,'p': 'ame o poema'}
    ]

    for p in palindromes:
        print('word:', p['p'])
        print('expected:', p['is'])
        assert p['is'] == stack_palindrome(p['p'])