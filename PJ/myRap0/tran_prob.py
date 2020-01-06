# -*- coding:utf-8 -*-
import jieba
import codecs
import re
import nltk
from nltk import *
import collections
from collections import Counter
import random
import xpinyin
from xpinyin import Pinyin
import numpy as np # numpy数据处理库
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库

#处理polished_lyric.txt，将分词结果存入words
file = codecs.open("polished_lyric.txt", 'r', 'utf-8')
content = file.read()
pattern=re.compile(r'[^a-zA-Z\u4e00-\u9fa5]')
content = re.sub(pattern, "", content)  # 去除所有非字母和汉字的字符
file.close()
print(content)
seg_list = jieba.cut(content)
words = [word for word in seg_list]
print(' '.join(words))
print(len(words))

#把转移频率存入字典tran_prob_dict
tran_prob_dict=dict()
# 生成转移矩阵
def get_tran_prob_dict():
    bigrams = nltk.bigrams(words)
    freq_dict = nltk.ConditionalFreqDist(bigrams)
    for (curr, curr_dict) in freq_dict.items():
        tran_prob_dict[curr] = {}
        # 当前词所有组合频数之和
        curr_total = sum(freq for (succ, freq) in curr_dict.items())
        # 所有下一个词出现的频率
        for succ in curr_dict:
            tran_prob_dict[curr][succ] = curr_dict[succ] / curr_total
            #print(curr, succ, tran_prob_dict[curr][succ])
get_tran_prob_dict()
for succ in tran_prob_dict['想要']:
    print(succ,tran_prob_dict['想要'][succ])

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#数据
name=[]
colleges=[]
count=0
#file = codecs.open("stop_words_zh.txt", 'r', 'utf-8')
#content3 = file.read()
stop_words=['的']
for item in tran_prob_dict['想要']:
    if item not in stop_words:
        name.append(item)
        colleges.append(tran_prob_dict['想要'][item])
        count+=1
        if count==15:
            break


#图像绘制
fig,ax=plt.subplots()
b=ax.barh(np.arange(len(name)),colleges,color='#FF7F00')
myfont = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)

ax.set_title(u'‘想要’的后继词的分布', fontproperties=myfont)

#添加数据标签
for rect in b:
    w=rect.get_width()
    ax.text(w,rect.get_y()+rect.get_height()/2,'%2f'%w,ha='left',va='center')

#设置Y轴刻度线标签
ax.set_yticks(np.arange(len(name)))
#font=FontProperties(fname=r'/Library/Fonts/Songti.ttc')
ax.set_yticklabels(name,fontproperties=myfont)

plt.savefig('tran_prob.png')
plt.show()
#plt.savefig('tran_prob.png')  # 放在show后面会保存一片空白