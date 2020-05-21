# encoding:utf-8
import os
import shutil
import struct
import binascii
import pdb


class Baidu(object):
    def __init__(self, originfile, txt_file):
        self.originfile = originfile
        self.lefile = originfile + '.le'
        self.txtfile = txt_file
        self.buf = [b'0' for x in range(0, 2)]
        self.listwords = []

    # 字节流大端转小端
    def be2le(self):
        of = open(self.originfile, 'rb')
        lef = open(self.lefile, 'wb')
        contents = of.read()
        contents_size = contents.__len__()
        mo_size = (contents_size % 2)
        # 保证是偶数
        if mo_size > 0:
            contents_size += (2 - mo_size)
            contents += contents + b'0000'
        # 大小端交换
        for i in range(0, contents_size, 2):
            self.buf[1] = contents[i]
            self.buf[0] = contents[i + 1]
            le_bytes = struct.pack('2B', self.buf[0], self.buf[1])
            lef.write(le_bytes)
        # print('写入成功转为小端的字节流')
        of.close()
        lef.close()

    def le2txt(self):
        lef = open(self.lefile, 'rb')
        txtf = open(self.txtfile, 'w')
        # 以字符串形式读取转成小端后的字节流，百度词典的起始位置为0x350
        # le_bytes = lef.read().hex()[0x350:]  # baidu
        le_bytes = lef.read().hex()[0x2628:]  # sougou
        i = 0
        while i < len(le_bytes):
            result = le_bytes[i:i + 4]
            i += 4
            #将所有字符解码成汉字，拼音或字符
            content = binascii.a2b_hex(result).decode('utf-16-be')
            #判断汉字
            if '\u4e00' <= content <= '\u9fff':
                self.listwords.append(content)
            else:
                if self.listwords:
                    word = ''.join(self.listwords)
                    if len(word) > 1:
                        txtf.write('{}\n'.format(word))
                    # print(word)
                self.listwords = []
        # print('写入txt成功')
        lef.close()
        txtf.close()


def remove_repeat(out_path, ok_dict):

    dct = {}
    with open(ok_dict, 'w') as w:
        for txt in os.listdir(out_path):
            txt_path = os.path.join(out_path, txt)
            with open(txt_path, 'r') as f:
                for l in f.readlines():
                    name = l.strip('\n')
                    if name not in dct.keys():
                        dct[name] = 0
                        w.write('{} {}\n'.format(name, 201))
    # print(dct.keys())
    # print(l.strip('\n'))


def main():
    # path = "./scel/地名词库.scel"
    scel_path = "./scel/"
    out_path = "./txt"
    ok_dict = './ok.txt'
    if os.path.isdir(out_path):
        shutil.rmtree(out_path)
    os.mkdir(out_path)

    for f_name in os.listdir(scel_path):
        # print(os.path.join(scel_path, f_name))
        new_name = os.path.join(scel_path, f_name)
        txt_name = os.path.join(out_path, f_name[:-4] + 'txt')
        print(txt_name)
        # pdb.set_trace()

        bd = Baidu(new_name, txt_name)
        bd.be2le()
        bd.le2txt()
        if os.path.isfile(new_name + '.le'):
            os.remove(new_name + '.le')

    remove_repeat(out_path, ok_dict)


if __name__ == '__main__':
    main()
