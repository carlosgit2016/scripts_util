def run(b):

    line_s=len(str(2**len(b)))+1 if len(str(2**len(b)))+1 > 4 else 4
    bit_string=""
    calc_string=""
    res_string=""
    empty_spaces=' '*line_s
    for x in range(len(b)):
        bit_string+='{:^{line}}'.format(b[x], line=line_s)
        calc_string+='{:^{line}}'.format(f'2^{x}', line=line_s)
        res_string+='{:^{line}}'.format(str(2**x), line=line_s)
    
    print(line_s)
    print(bit_string)
    print(calc_string)
    print(res_string)

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
