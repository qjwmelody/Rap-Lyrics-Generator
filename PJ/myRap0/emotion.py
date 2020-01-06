# -*- coding:utf-8 -*-
import codecs
import re
from snownlp import SnowNLP

rapper_playlist_list = [('红花会', 799977314),
               ('PGone', 447516565),
               ('VaVa', 808488091),
               ('艾福杰尼', 510860563),
               ('BooM黄旭', 714593343),
               ('Bridge', 639741735),
               ('GAI爷', 557229147),
               ('TizzyT', 462399965),
               ('JonyJ', 49527655),
               ('小青龙', 808976784),
               ('辉子', 714778058),
               ('孙八一',776141176),
               ('谢帝', 55433749),
               ('马思维', 155059572),
               ('Mc光光', 126482980),
               ('满舒克', 110228333)
               ]
for (rapper,id) in rapper_playlist_list:
    file = codecs.open('lyrics/'+rapper+".txt", 'r', 'utf-8')
    content = file.read()
    content = re.sub("[^\u4e00-\u9fa5]+", "", content)  # 去除所有非中文字符、非空字符
    s = SnowNLP(content)
    print(rapper,s.sentiments)
    file.close()
