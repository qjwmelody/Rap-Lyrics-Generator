# -*- coding:utf-8 -*-
import requests
import json
import time
#from lxml import etree
from lxml import html
etree=html.etree
import codecs
import re

rapper_list2 = ['红花会', 'pgone', 'vava', '艾福杰尼', '黄旭', 'jonyj','bridge', 'gai', 'tt', '小青龙', '辉子', '孙八一', '谢帝', '马思唯',
                '光光', '满舒克']
file = codecs.open("JonyJ_comments.txt", 'r', 'utf-8')
content3 = file.read()
# 识别每一个歌手
content4 = re.sub("PGone", "pgone", content3)
content4 = re.sub("VaVa|VAVA", "vava", content3)
content4 = re.sub("Bridge", "bridge", content3)
content4 = re.sub("Gai|GAI", "gai", content3)
content4 = re.sub("Tizzy|TT", "tt", content3)
content4 = re.sub("[JJ|'Jony'|JonyJ|豆芽]", "jonyj", content3)

r_to_jonyj = dict()


comments = content3.splitlines()

for rapper0 in rapper_list2:
    r_to_jonyj[rapper0] = 0  # 初始化共现次数为0
    for comment in comments:  # 处理每条评论
        if rapper0 in comment:  # 如果提到jonyj
            r_to_jonyj[rapper0] += 1
            #print('jonyj',rapper0,r_to_jonyj[rapper0])

for rapper0 in r_to_jonyj:
    print(rapper0,r_to_jonyj[rapper0])

"""
#filename = 'JonyJ_comments.txt'
#f=codecs.open(filename, 'w','utf-8')

class GetComments(object):
    def __init__(self):
        self.headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'Connection': "keep-alive",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        # 构造会话
        self.session = requests.session()
        # 设置代理
        self.proxies = {
            'http': 'http://183.62.22.220:3128',
            'http': 'http://118.190.95.35:9001',
            'http': 'http://61.135.217.7:80',
            'http': 'http://106.75.9.39:8080',
            'http': 'http://118.190.95.43:9001',
            'http': 'http://121.31.157.94:8123',
            'http': 'http://115.46.67.248:8123',
            'http': 'http://182.88.14.243:8123'
        }

    def get_json(self, song_id, offset):
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_%s?limit=20&offset=%s' % (song_id, offset)
        print(url)
        responses = self.session.get(url, headers=self.headers).content
        json_dict = json.loads(responses)
        return json_dict

    def structure_url(self, song_id, song_name):
        json_dict = self.get_json(song_id, 0)
        print(json_dict)
        comments_num = int(json_dict['total'])  # 获取评论总数目
        if not comments_num % 200:
            page = comments_num / 200
        else:
            page = int(comments_num / 200) + 1
        for i in range(page):
            comments_list = []
            json_dict = self.get_json(song_id, i * 200)
            print(page * 200)
            for item in json_dict['comments']:
                comment = item['content'].replace("\n","")  # 获取评论内容 并去掉换行符
                liked_count = item['likedCount']  # 点赞总数
                comment_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(item['time'] / 1000))  # 获取评论时间
                comment_info = comment_time + ' ' + str(liked_count) + ' ' + comment + '\n'
                f.write(comment_info)
                comments_list.append(comment_info)
            print('第 %s 页获取完成.' % i)

    def get_songs_id(self, url):
        html = self.session.get(url, headers=self.headers)
        text = etree.HTML(html.text)
        # print(html.text)
        songs_name = text.xpath('//div[@id="hotsong-list"]/div[@class="f-cb"]/div/ul//a/text()')
        songs_id = text.xpath('//div[@id="hotsong-list"]/div[@class="f-cb"]/div/ul//a/@href') # 获取歌曲id
        songs_id = [s_id[9:] for s_id in songs_id]
        print(songs_name)
        print(songs_id)
        for i in range(len(songs_name)):
            self.structure_url(songs_id[i], songs_name[i])
            print('正在收集 %s 的评论' % songs_name[i])

rapper_list = [('红花会', 799977314),
               ('PGone', 447516565),
               ('VaVa', 1038099),
               ('艾福杰尼', 12127564),
               ('Boom黄旭', 12065096),
               ('布瑞吉Bridge', 12493701),
               ('GAI周延', 1211046),
               ('Tizzy T', 1204010),
               ('Jony J', 784257),
               ('小青龙', 12199576),
               ('辉子', 12371082),
               ('孙八一',1089111),
               ('谢帝', 847107),
               ('马思唯', 1132392),
               ('Mc光光', 187903),
               ('满舒克', 188141)
               ]


if __name__ == '__main__':
    for (rapper,id) in rapper_list:
        filename = rapper+'.txt'
        f = codecs.open(filename, 'w', 'utf-8')
        singer_url = 'https://music.163.com/artist?id='+len(id)
        spider = GetComments()
        spider.get_songs_id(singer_url)
        f.close()
"""