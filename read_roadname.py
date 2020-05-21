
with open('./road_name/road_ok.txt', 'w') as w:
    with open('./road_name/road_name.txt', 'r') as f:
        dct = {}
        for l in f.readlines():
            new_l = l.strip('\n')
            l_split = new_l.split('|')
            for ll in l_split:
                if ll not in dct.keys():
                    dct[ll] = 0
                    w.write('{} {}\n'.format(ll, 205))
                    # print(ll)
