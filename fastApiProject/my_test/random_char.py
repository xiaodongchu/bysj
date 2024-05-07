import random

from pyperclip import copy

pinyin_list = list("āáǎàōóǒòēéěèīíǐìūúǔùǖǘǚǜü")
# 全角标点
punctuation_list = list("，。、；’【】、-=！@#￥%……&*（）——+{}|：”《》？")
# 半角标点
punctuation_list.extend(list(",."))
# punctuation_list.extend(list("/;'[]\\-=!@#$%^&*()_+{}|:\"<>?"))
# 数字
number_list = list("0123456789")
# 字母
letter_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
# 中文
chinese_chars = [chr(i) for i in range(0x4e00, 0x9fa5)]


def random_char(lenth):
    """
    随机生成指定长度的字符串
    :param lenth: int
    :return: str
    """
    res = ""
    while len(res) < lenth:
        r = random.random()
        if r < 0.05:
            r0 = random.randint(0, 20)
            r1 = random.random()
            if r1 < 0.5:
                temp_list = pinyin_list + letter_list
                for j in range(r0):
                    res += random.choice(temp_list)
            elif r1 < 0.7:
                for j in range(r0):
                    res += random.choice(letter_list)
            else:
                for j in range(r0):
                    res += random.choice(number_list)
        elif r < 0.1:
            res += random.choice(punctuation_list)
        else:
            res += random.choice(chinese_chars)
    return res


if __name__ == '__main__':
    while True:
        try:
            a = int(input())
        except:
            continue
        a = random_char(a)
        print(a)
        copy(a)
