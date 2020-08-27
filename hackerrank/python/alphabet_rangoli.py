def print_rangoli(size):
    # your code goes here
    l_size = (size * 4) - 3
    lines = []
    for l in range(1, size + 1):  # 1
        line = ''
        for f_part in range(0, l):  # 0 , 1
            line += chr(size + 96 - f_part)
            if len(line) < l_size:
                line += '-'
        for s_part in range(l - 1, 0, -1):  # 1 , 0, -1 | 2, 0, -1  2 1line = ''
            line += chr(size + 97 - s_part)
            if len(line) < l_size:
                line += '-'
        lines.append(line.center(l_size, '-'))


    lines_reverse = lines[:size - 1]
    lines_reverse.reverse()
    lines.extend(lines_reverse)
    print("\n".join(lines))

if __name__ == '__main__':
    n = int(input())
    print_rangoli(n)
