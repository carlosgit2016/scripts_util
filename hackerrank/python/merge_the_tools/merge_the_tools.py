def merge_the_tools(string, k):
    for i in range(0, len(string), k):
        t = string[i:i+k]
        u = ""
        for j in range(len(t)):
            if j == 0:
                u+=t[j]
            elif t[j] not in u:
                u+=t[j]

        print(u)

if __name__ == "__main__":
    merge_the_tools('AABCAAADA', 3)
