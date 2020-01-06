# -*- coding:utf-8 -*-
import jieba
import jieba.posseg as pseg
import codecs
import re
import nltk
from nltk import *
import collections
from collections import Counter
import random
import xpinyin
from xpinyin import Pinyin

# 处理polished_lyric.txt，将分词结果存入words
file = codecs.open("polished_lyric.txt", 'r', 'utf-8')
content = file.read()
file.close()
content1=re.sub(" ","",content)  # 去除所有空格
content1 = re.sub("[^\u4e00-\u9fa5\s]+", "", content1)  # 去除所有非中文字符、非空字符

# 词性标注（标注每一句的第一个词和最后一个词）
sens=content1.splitlines()
start_words=dict()
last_words=dict()
remove=['作曲','作词']
sen_count=0
for sen in sens:
    if sen=='':
        continue
    sen_words=jieba.cut(sen)
    sen_words=' '.join(sen_words)
    sw=sen_words.split(' ', 1)[0]
    lw=sen_words.split(' ')[-1]
    if sw in remove:
        continue
    if sw in start_words:
        start_words[sw]+=1
    if lw in last_words:
        last_words[lw]+=1
    else:
        start_words[sw]=0
        last_words[lw]=0
    sen_count+=1 # 总句数+1
for w in start_words:
    start_words[w]/=sen_count
for w in last_words:
    last_words[w]/sen_count


content = re.sub("\s+", "", content)  # 去空
content = re.sub("[^\u4e00-\u9fa5]+", "", content)  # 去除所有非中文字符

#print(content)
seg_list = pseg.cut(content)
# print(' '.join(seg_list))  #generator只能用一次
words_tag = [word for word in seg_list]  #所有的词+词性
words=[word for (word,flag) in words_tag]
#print(' '.join(words))
#print(len(words))

#把每个词的词性标注存入字典
tagger_dict=dict()
for (word,flag) in words_tag:
    tagger_dict[word]=flag
#print(len(tagger_dict))

#把每个词出现频率存入字典freq_dict
freq_dict = dict()
for item in FreqDist(words).most_common():
    #print(item[0], item[1])
    freq_dict[item[0]]=item[1]
#print(len(freq_dict))
#for word in freq_dict:
    #print(word,freq_dict[word])


#把转移频率存入字典tran_prob_dict
tran_prob_dict=dict()
# 生成转移矩阵
def get_tran_prob_dict():
    bigrams = nltk.bigrams(words)
    freq_dict = nltk.ConditionalFreqDist(bigrams)
    for (curr, curr_dict) in freq_dict.items():
        #print(curr,freq_dict[curr].most_common(1))
        tran_prob_dict[curr] = {}
        # 当前词所有组合频数之和
        curr_total = sum(freq for (succ, freq) in curr_dict.items())
        # 所有下一个词出现的频率
        for succ in curr_dict:
            tran_prob_dict[curr][succ] = curr_dict[succ] / curr_total
            #print(curr, succ, tran_prob_dict[curr][succ])
get_tran_prob_dict()

def get_most_prob_succ(curr):
    max_prob=0
    for item in tran_prob_dict[curr]:
        if tran_prob_dict[curr][item]>max_prob:
            max_prob=tran_prob_dict[curr][item]
            print(curr,item,max_prob)
            return item



class MyFormat:
    def __init__(self):
        self.num_sen = 0  # 总行数
        self.len_sen = {}  # 每行的字数
        #self.cfd = dict()  # 转移矩阵
        self.yunjiao = 'o'  # 每一句都压的随机生成的韵脚
        self.rap = []  # 最终生成结果

    # 读取某一段rap的格式（主要是每一句的字数），便于模仿创作
    # 默认一行就是一句
    def load_format(self, filename):
        file = codecs.open(filename, 'r', 'utf-8')
        for line in file:
            line = re.sub("\s", "", line)
            self.len_sen[self.num_sen] = len(line)
            # print(line, self.len_sen[self.num_sen])
            self.num_sen += 1
        self.len_sen[0] -= 1
        i = 0


    # 检查一个词是否押韵（即是否在该韵脚对应的数据库里面）
    def check_yayun(self, word):
        # 这里先写成直接判断的格式
        # 切片取得押韵字数
        yunjiao2 = self.yunjiao.split('-')
        num_yayun = len(yunjiao2)
        if len(word) < num_yayun:
            return False
        n = num_yayun * (-1)
        word = word[n:]

        p = Pinyin()
        pin = p.get_pinyin(word)
        word_pin = pin.split('-')

        word_yun = {}
        pattern = r"an|ui|uan|ian|iu|eng|ue|ing|a|ei|en|uo|ye|in|ou|ao|uang|ong|ang|ai|ua|uai|iao|ia|ie|iong|i|er|e|u|un|iang|o|qu|xu|yu"
        i = 0
        while i < num_yayun:
            ret = re.findall(pattern, word_pin[i])
            word_yun[i] = ret
            i += 1

        i = 0
        flag = True
        while i < num_yayun:
            if yunjiao2[i] != word_yun[i][0]:
                flag = False
            i += 1
        return flag

        '''
        RhymeIndex = [('1', ['a', 'ia', 'ua']),
                      ('2', ['ai', 'uai']),
                      ('3', ['an', 'ian', 'uan']),
                      ('4', ['ang', 'iang', 'uang']),
                      ('5', ['ao', 'iao']),
                      ('6', ['e', 'o', 'uo']),
                      ('7', ['ei', 'ui']),
                      ('8', ['en', 'in', 'un']),
                      ('9', ['eng', 'ing', 'ong', 'iong']),
                      ('10', ['er']),
                      ('11', ['i']),
                      ('12', ['ie', 'ye']),
                      ('13', ['ou', 'iu']),
                      ('14', ['u']),
                      ('16', ['ue']),
                      ('15', ['qu', 'xu', 'yu'])]
        '''


    # 马尔可夫模型递归生成
    def gen_markov(self, word, sen_pos, word_pos):
        # 第sen_pos句，第word_pos个词
        if sen_pos >= self.num_sen:
            return True
        if word not in tran_prob_dict:
            print("数据库中不含该词")
            return False
        else:
            choices = [item for item in tran_prob_dict[word]]
            random.shuffle(choices)
            for succ in choices:
                if word_pos + len(word) == self.len_sen[sen_pos]:  # 当前词刚好是最后一个，换行
                    sen_pos2 = sen_pos + 1
                    word_pos2 = 0
                    if sen_pos2 >= self.num_sen:
                        return True
                    if len(succ) > self.len_sen[sen_pos2]:  # 如果下一句话的第一个词就超长
                        continue
                    if succ not in start_words:
                        if succ==choices[-1]: #如果到了最后一个
                            succ=random.choice(list(start_words))
                            self.rap.append(succ)
                        else:
                            continue
                    else:
                        self.rap.append(succ)
                elif word_pos + len(word) + len(succ) > self.len_sen[sen_pos]:  # 加上下一个词后超出范围，换词
                    continue
                elif word_pos + len(word) + len(succ) == self.len_sen[sen_pos]:  # 下一个词刚好是结尾，检查押韵
                    if succ not in last_words:
                        if succ!=choices[-1]:
                            continue
                    if not self.check_yayun(succ):  # 检查是否押韵
                        continue
                    else:
                        self.rap.append(succ)
                    # self.rap.append('\n')
                    sen_pos2 = sen_pos
                    word_pos2 = word_pos + len(word)
                else:  # 下一个词也不是最后一个
                    self.rap.append(succ)
                    sen_pos2 = sen_pos
                    word_pos2 = word_pos + len(word)
                if self.gen_markov(succ, sen_pos2, word_pos2):
                    return True
                self.rap.pop()  # 返回上一个词
            return False



if __name__ == '__main__':
    myrap = MyFormat()
    myrap.load_format("模板_差不多先生.txt")
    #start = '我'
    start = input("\n\nWhat do you want to start your rap with?\n > ")
    myrap.rap.append(start)
    myrap.gen_markov(start, 0, 0)
    print("Alright, here's your rap:")
    rap = ''.join(myrap.rap)
    i = 0
    k = 0
    while i < myrap.num_sen:
        j = 0
        while j < myrap.len_sen[i]:
            print(rap[k], end='')
            k += 1
            j += 1
        print('\r')
        i += 1



