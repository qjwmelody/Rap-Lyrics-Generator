# -*- coding:utf-8 -*-
import jieba
import codecs
import re
import nltk
from nltk import *
from nltk.corpus import stopwords
import collections
from collections import Counter
import random
import xpinyin
from xpinyin import Pinyin
import numpy as np # numpy数据处理库
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库

# 读所有歌词
fn=open('init_lyric.txt','r',encoding='utf-8')
content=fn.read()
fn.close()

words=[]

# 获取中文
pattern1=re.compile(r'[^\u4e00-\u9fa5]+')
content1=re.sub(pattern1,'',content)
#print(content1)
# 文本分词
seg_list = jieba.cut(content1)
file = codecs.open("stop_words_zh.txt", 'r', 'utf-8')
content3 = file.read()
stop_words=content3.splitlines()
for word in seg_list:
    if word not in stop_words:
        words.append(word)
file.close()

# 获取英文
pattern2=re.compile(r'[^a-zA-Z]+')
content2=re.sub(pattern2,' ',content)
#print(content2)
#tokens = nltk.word_tokenize(content2)
tokens=content2.split(' ')
stoplist=stopwords.words('english')
stoplist.append('I')
for word in tokens:
    if word not in stoplist:
        words.append(word)

#词频统计
word_counts=collections.Counter(words)
word_counts_top=word_counts.most_common()
print(word_counts_top)

#词频展示
background=np.array(Image.open('wordcloud4.jpg'))
wc=wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simhei.ttf',  #字体
    mask=background,  # 背景图
    background_color='white',  #背景颜色
    max_words=800,  # 最多显示词数
    max_font_size=700,  #字体最大值
    min_font_size=20
)

wc.generate_from_frequencies(word_counts)
image_colors=wordcloud.ImageColorGenerator(background)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
wc.to_file('ciyun.png')
plt.show()
