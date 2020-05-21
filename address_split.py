# encoding=utf-8
import shlex
import jieba
import pdb


def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace = ','
    lex.whitespace_split = True
    lex.commenters = ','
    return list(lex)


def stopwordslist():
    stopwords = [
        line.strip()
        for line in open('./ignore.txt', encoding='UTF-8').readlines()
    ]
    return stopwords


def linkwords(list_words):

    lst_char = ['-']
    in_words = list(set(lst_char).intersection(set(list_words)))

    for word in in_words:
        for _ in range(list_words.count(word)):

            idx = list_words.index(word)
            idx_insert = ''.join(list_words[(idx - 1):(idx + 2)])
            if len(list_words) >= (idx + 2):
                list_words.remove(list_words[idx + 1])
            list_words.remove(list_words[idx])
            list_words.remove(list_words[idx - 1])
            list_words.insert(idx - 1, idx_insert)

    return list_words


def get_mergewordslist():
    mergewords = list(
        set([
            line.strip()
            for line in open('./merge.txt', encoding='UTF-8').readlines()
        ]))
    return mergewords


def mergewords(list_words, lst_mergeword):

    in_words = list(set(list_words).intersection(set(lst_mergeword)))
    for word in in_words:
        # print(list_words)
        # print(lst_mergeword)
        # print(in_words)
        for _ in range(list_words.count(word)):
            idx = list_words.index(word)
            if idx != 0:
                idx_insert = ''.join(list_words[(idx - 1):(idx + 1)])
                # if len(list_words) >= (idx + 2):
                #     list_words.remove(list_words[idx + 1])
                list_words.remove(list_words[idx])
                list_words.remove(list_words[idx - 1])
                list_words.insert(idx - 1, idx_insert)

        # print(list_words)
        # pdb.set_trace()

    return list_words


def split_address(address_path):

    stopwords = stopwordslist()
    lst_mergeword = get_mergewordslist()
    # print(stopwords)
    # pdb.set_trace()
    with open('./split.txt', 'w') as w:
        with open(address_path, 'r') as f:
            for l in f.readlines():
                new_l = l.strip('\n')
                lst_poi = [i.replace('"', '') for i in newSplit(new_l)]
                if len(lst_poi) == 3:
                    w.write('{}\n'.format(new_l))
                    seg_list = jieba.cut(lst_poi[2], cut_all=False)
                    lst = list(seg_list)
                    print("|".join(lst))  # 精确模式
                    w.write('jieba: {}\n'.format("|".join(lst)))

                    # del stop words
                    list_stop = [i for i in lst if i not in stopwords]

                    # link words
                    list_links = linkwords(list_stop)

                    list_merges = mergewords(list_links, lst_mergeword)

                    w.write('ok:    {}\n'.format("|".join(list_merges)))

                    w.write('{}\n'.format('-' * 40))
                # print('-' * 40)


def main():
    dct_path = './qinhuangdao/dict/roadname_dict.txt'
    address_path = './qinhuangdao/poi.txt'

    jieba.load_userdict(dct_path)
    split_address(address_path)


if __name__ == "__main__":
    main()
