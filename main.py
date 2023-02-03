with open('./code_sources_v3.txt', encoding='gbk') as cs:
    line = cs.readline()
    set_c = ''.join(sorted(set(line)))
    print(set_c)
    print(len(list(line)))
    print(len(set(line)))
