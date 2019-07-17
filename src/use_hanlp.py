from pypinyin import pinyin, Style
from jpype import JClass

import pyhanlp
import random
import os
import re

PATH = '../../data_aishell/transcript'
Jpinyin = JClass('com.hankcs.hanlp.dictionary.py.PinyinDictionary')

# 原始文件位置
FileName = 'aishell_transcript_v0.8.txt'
# 标准文件位置
StandardPath = '../../data_aishell'
TrainStandardFile = 'aishell_train.txt'
TestStandardFile = 'aishell_test.txt'
DevStandardFile = 'aishell_dev.txt'
# 输出目标文件1
OutPutFile_by_hanlp = 'pinyin_by_hanlp.txt'
# 输出目标文件2
OutPutFile_by_pypinyin = 'pinyin_by_pypinyin.txt'
# 随机抽取1000条对比
RandomFile = 'Random1000.txt'

WavNameLength = 16

pinyinlist = []
hanzilist = []

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
        res.append([item])
    return res


def convertToPinyinByPinyin(hanzi):
    return pinyin(hanzi, style=Style.TONE3)


def get_standard_train_data():
    with open(os.path.join(StandardPath, TrainStandardFile)) as f1:
        for line in f1:
            line = line.split('\t')
            pinyinlist.append(line[1])
            hanzilist.append(line[2])


def get_standard_dev_data():
    with open(os.path.join(StandardPath, DevStandardFile)) as f1:
        for line in f1:
            line = line.split('\t')
            pinyinlist.append(line[1])
            hanzilist.append(line[2])


def get_standard_test_data():
    with open(os.path.join(StandardPath, TestStandardFile)) as f1:
        for line in f1:
            line = line.split('\t')
            pinyinlist.append(line[1])
            hanzilist.append(line[2])


def main():
    get_standard_train_data()
    get_standard_dev_data()
    get_standard_test_data()

    with open(os.path.join(PATH, OutPutFile_by_hanlp), 'w+') as f1:
        with open(os.path.join(PATH, OutPutFile_by_pypinyin), 'w+') as f2:
            with open(os.path.join(PATH, RandomFile), 'w+') as f:

                count = 0
                count1 = 0
                count2 = 0
                num = 0
                Len = len(pinyinlist)
                result1 = ""
                result2 = ""
                valuelist = ""

                klist = random.sample(range(Len), 1000)
                for i in range(Len):
                    hanzi = hanzilist[i]
                    pin = pinyinlist[i]

                    # 讲标准进行处理
                    pin = pin.split(' ')
                    res = []
                    for item in pin:
                        res.append([item])
                    pin = str(res)

                    # 过滤换行符空格等
                    hanzi = filter(hanzi)
                    res1 = str(convertToPinyinByHanlp(hanzi))
                    res2 = str(convertToPinyinByPinyin(hanzi))
                    result1 += res1 + '\n'
                    result2 += res2 + '\n'

                    # 不同个数
                    num += 1
                    if res1 != res2:
                        count += 1
                    if res1 != pin:
                        count1 += 1
                    if res2 != pin:
                        count2 += 1

                    if i in klist:
                        if res1 != res2:
                            valuelist += '----------------------Error---------------------\n'
                        valuelist += "汉字：" + hanzi + '\n' + "Hanlp    : " + res1 + '\n' + "Pypinyin : " + res2 + '\n'
                f.writelines(valuelist)
            f2.writelines(result2)
        f1.writelines(result1)

    print("两两不相等的数量如下:")
    print("Hanlp不同于Pypinyin:    " + str(count / num))
    print("Hanlp不同于Standard:    " + str(count1 / num))
    print("Pypinyin不同于Standard: " + str(count2 / num))
    print('-----------end-----------')


if __name__ == '__main__':
    main()
