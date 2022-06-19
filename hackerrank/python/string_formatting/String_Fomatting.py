def print_formatted(number):
    b = convert_from_dec_to_bin(number)

    for i in range(number):
        maxB = get_spaces(len(str(b)) - len(str(i + 1)))
        fN = maxB + str(i + 1)
        print(print_with_space(i + 1, b), print_with_space(convert_from_dec_to_octa(i + 1), b), print_with_space(convert_from_dec_to_hex(i + 1), b), print_with_space(convert_from_dec_to_bin(i + 1), b))

def convert_from_dec_to_octa(number):
    return convert_from_dec_to_x(number, 8)
def convert_from_dec_to_hex(number):
    return convert_from_dec_to_x(number, 16)
def convert_from_dec_to_bin(number):
    return convert_from_dec_to_x(number, 2)

def convert_from_dec_to_x(number, divisor):
    if divisor == 8:
        return converter(oct, 'o', number)
    elif divisor == 16:
        return (converter(hex, 'x', number)).upper()
    elif divisor == 2:
        return converter(bin, 'b', number)

def converter(f, l, n):
    return f(n).split(l)[-1]

def wrapper_print(l, m):
    s = ""
    for i in l:
        s += print_with_space(i, m)
    return s

def print_with_space(n, mbinary):
    maxB = get_spaces(len(str(mbinary)) - len(str(n)))

    return maxB + str(n)

def get_spaces(n):
    spaces = ""
    for i in range(n):
        spaces += " "
    return spaces
