from pypinyin import pinyin, Style
from jpype import JClass

import pyhanlp
import random
import os
import re

Jpinyin = JClass('com.hankcs.hanlp.dictionary.py.PinyinDictionary')

PATH = '/home/chengli/matrix/speech_data'

InPutFile = '/data/data_thchs30/data/*.trn'

hanzilist = []
pinyinlist = []

def filter(str):
    return re.sub("[\\n\\s]", "", str)

def convertToPinyinByHanlp(hanzi):
    hanzi = filter(hanzi)
    pinyin1 = Jpinyin.convertToPinyin(hanzi)
    res = []
    for item in list(pinyin1):
        item = str(item)
        if '5' in str(item):
            item = item.replace('5', '')
        res.append(item)
    return res


def convertToPinyinByPinyin(hanzi):
    res = pinyin(hanzi, style=Style.TONE3)
    # print(res)
    res = re.sub("[\s'\[\]]", '', str(res))
    # print(res)
    res1 = res.split(",")
    return res1


def main():
    dirname = os.path.join(PATH, 'data/data_thchs30/data')
    count = 0
    count1 = 0
    count2 = 0
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            if filename[-4:] == '.trn':
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                # print(filename[-4:])
                with open(apath) as f:
                    text = f.readlines()
                    hanzi = filter(text[0])
                    pinyin = re.sub("[\\n]", "", text[1])
                    pinyin = pinyin.split(' ')
                    res = []
                    for item in pinyin:
                        if '5' in str(item):
                            item = item.replace('5', '')
                        res.append(item)
                    pin = res

                    print(pin)
                    pinyin1 = convertToPinyinByHanlp(hanzi)
                    pinyin2 = convertToPinyinByPinyin(hanzi)
                    print(pinyin1)
                    print(pinyin2)
                    length = len(pinyin)
                    for i in range(length):
                        count += 1
                        if pinyin1[i] != pinyin[i]:
                            count1 += 1
                        if pinyin2[i] != pinyin[i]:
                            count2 += 1
        print(count)
        print(count1)
        print(count2)
    print("Hanlp   : " + str(count1/count))
    print("Pypinyin: " + str(count2/count))


if __name__ == '__main__':
    main()