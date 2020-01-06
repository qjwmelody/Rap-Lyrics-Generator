# 爬取网易云音乐我的歌单里面所有歌曲的歌词

import json
import requests
import re
import urllib
from bs4 import *

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

f_all_init=open('init_lyric.txt','w',encoding='utf-8')
f_all_polished=open('polished_lyric.txt','w',encoding='utf-8')

for (rapper,id) in rapper_playlist_list:
    url = "http://music.163.com/playlist?id="+str(id)
    headers = {"Host": " music.163.com",
               "User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
               }
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read().decode
    soup = BeautifulSoup(html)
    print(soup.prettify())

    #打开.txt 把歌单中的歌词写入
    f=open('lyrics/'+rapper+'.txt','w',encoding='utf-8')

    for item in soup.ul.children:
        # 取出歌单里歌曲的id  形式为：/song?id=11111111
        song_id = item('a')[0].get("href", None)
        # 歌曲名称
        song_name = item.string
        # 利用正则表达式提取出song_id的数字部分sid
        pat = re.compile(r'[0-9].*$')  # 提取模式为全都为数字的字符串
        sid = re.findall(pat, song_id)[0]  # 提取歌曲ID
        # 打印歌曲ID以及名称
        print(sid + "-" + song_name)

        #歌词页面
        url = "http://music.163.com/api/song/lyric?"+"id="+str(sid)+"&lv=1&kv=1&tv=-1"
        html = requests.post(url)
        json_obj = html.text
        #歌词是一个json对象 解析
        j = json.loads(json_obj)
        #print(j)

        try:
            lyric = j['lrc']['lyric']
        except KeyError:
            lyric = "无歌词"
            tlyric="no lyric"

        pat = re.compile(r'\[.*\]|(\r\n)+')
        lrc = re.sub(pat, "", lyric)
        lrc1 = song_name + "-"+ rapper+ '\n' + lrc.strip()+ '\n\n\n'
        #print(lrc)
        f.write(lrc1)
        f_all_init.write(lrc1)

        pat2=re.compile(r'作曲.*\r')
        lrc2=re.sub(pat2,'',lrc)
        pat2 = re.compile(r'无歌词')
        lrc2 = re.sub(pat2, '', lrc2)
        
        f_all_polished.write(lrc2)

    f.close()
f_all_init.close()
f_all_polished.close()



"""
<ul class="f-hide">
         <li>
          <a href="/song?id=1325711347">
           喜新恋旧
          </a>
         </li>
         <li>
          <a href="/song?id=31260611">
           信仰
          </a>
         </li>
         <li>
          <a href="/song?id=534542490">
           奴隶
          </a>
         </li>
         <li>
          <a href="/song?id=520459701">
           想把你留在这里
          </a>
         </li>
         <li>
          <a href="/song?id=1325896303">
           My Man
          </a>
         </li>
         <li>
          <a href="/song?id=1325898283">
           28
          </a>
         </li>
         <li>
          <a href="/song?id=1325711344">
           连锁反应
          </a>
         </li>
         <li>
          <a href="/song?id=419374860">
           住你耳朵里
          </a>
         </li>
         <li>
          <a href="/song?id=530986052">
           返老还童
          </a>
         </li>
         <li>
          <a href="/song?id=436667978">
           慢慢来
          </a>
         </li>
         <li>
          <a href="/song?id=501220106">
           Almost Home
          </a>
         </li>
         <li>
          <a href="/song?id=1325711349">
           子弹口水
          </a>
         </li>
         <li>
          <a href="/song?id=1325896295">
           迷宫Intro
          </a>
         </li>
         <li>
          <a href="/song?id=491065931">
           甜葡萄 红眼睛
          </a>
         </li>
         <li>
          <a href="/song?id=1325896427">
           喽啰
          </a>
         </li>
         <li>
          <a href="/song?id=501220404">
           你看得见
          </a>
         </li>
         <li>
          <a href="/song?id=1325896298">
           How To Lie
          </a>
         </li>
         <li>
          <a href="/song?id=1325896319">
           泛滥
          </a>
         </li>
         <li>
          <a href="/song?id=1325896320">
           迷宫Outro
          </a>
         </li>
         <li>
          <a href="/song?id=449818593">
           Okay
          </a>
         </li>
         <li>
          <a href="/song?id=31134264">
           My City 南京
          </a>
         </li>
         <li>
          <a href="/song?id=449824583">
           物女金
          </a>
         </li>
         <li>
          <a href="/song?id=31260606">
           我与自己(feat.讲者)
          </a>
         </li>
         <li>
          <a href="/song?id=419373878">
           开门见山
          </a>
         </li>
         <li>
          <a href="/song?id=449818601">
           Fantasy
          </a>
         </li>
         <li>
          <a href="/song?id=26562526">
           Yes Day
          </a>
         </li>
         <li>
          <a href="/song?id=31260615">
           睡前老报纸[Bonus track]
          </a>
         </li>
         <li>
          <a href="/song?id=31260603">
           My City(feat.顾杰)
          </a>
         </li>
         <li>
          <a href="/song?id=31260613">
           What'll U Do[Bonus track]
          </a>
         </li>
         <li>
          <a href="/song?id=449818591">
           Intro
          </a>
         </li>
         <li>
          <a href="/song?id=439665556">
           Team Work
          </a>
         </li>
         <li>
          <a href="/song?id=449818596">
           So.Far.So.Good
          </a>
         </li>
         <li>
          <a href="/song?id=482724567">
           Big Things Start Small
          </a>
         </li>
         <li>
          <a href="/song?id=419373881">
           无业游民
          </a>
         </li>
         <li>
          <a href="/song?id=29740024">
           改变
          </a>
         </li>
         <li>
          <a href="/song?id=26577093">
           众人皆醉我独醒
          </a>
         </li>
         <li>
          <a href="/song?id=31260610">
           时光列车
          </a>
         </li>
         <li>
          <a href="/song?id=31861477">
           忙先生
          </a>
         </li>
         <li>
          <a href="/song?id=31260607">
           安格拉夏
          </a>
         </li>
         <li>
          <a href="/song?id=26577095">
           口袋里的秘密
          </a>
         </li>
         <li>
          <a href="/song?id=31260595">
           J Hood
          </a>
         </li>
         <li>
          <a href="/song?id=31260605">
           记忆碎片
          </a>
         </li>
         <li>
          <a href="/song?id=449818599">
           Skit
          </a>
         </li>
         <li>
          <a href="/song?id=31260600">
           Come Here RMB
          </a>
         </li>
        </ul>
    """



"""
[by:松弛有度]
[ti:come here R M B]
[ar:乔尼 JONY J]
[al:J Hood Mixtape ]
[00:10.79]Verse1:
[00:14.83]他们就是几个数字
[00:20.21]躺在你账户 让你度日
[00:21.91]没了它 你寸步难行
[00:23.81]更别想你要的hood dream
[00:26.28]那时候你 还不知道
[00:28.12]RMB 有多重要
[00:30.43]直到开始 虚荣心围绕
[00:32.29]需要自己解决暖饱
[00:34.39]你hustle hustle到断了腿
[00:36.39]违心话说到烂了嘴
[00:38.37]觉得脑袋好像是灌了水
[00:40.39]keep going 是为了谁
[00:42.40]你稍微有点放松停下
[00:44.67]包围你的就是生活廉价
[00:46.85]是该一意孤行还是变的圆滑
[00:48.46]他们说看 都是钱呐
[00:50.70]come here RMB
[00:52.58]u never know da how i need
[00:54.66]有人靠它勉强维持生计
[00:56.52]有人用它Light a weed
[00:58.74]你說過討厭現實勢利
[01:00.56]可是現在你討厭你自己
[01:02.93]你該有個信仰甚至對它也是
[01:06.70]失敗了算什麽大不了就多試幾次
[01:10.36]keep chase dream RMB會來的請相信
[01:14.67]過程裡是你留下的汗跟你的不信命[我說]
[01:18.37]你該有個信仰甚至對它也是
[01:22.73]失敗了算什麽大不了就多試幾次
[01:26.63]keep chase dream RMB會來的請相信
[01:30.89]過程裡是你留下的汗跟你的不信命
[01:40.49]Verse2：
[01:50.59]如果要做就做next big
[02:09.96]用你的夢想帶來RMB
[02:11.95]请你脚踏实地 打破所有质疑
[02:13.88]因为你想要的不止是那些纸币
[02:16.19]赚到了money还要赚到了夸奖
[02:18.16]给现实狠狠甩上一巴掌
[02:20.23]跟现实对抗 到最后都是站着
[02:22.22]也把它送给当初唱衰你的看客
[02:24.22]把时间 都花在hustle里面
[02:26.20]不断的赚钱不止为了活的体面
[02:28.24]为自己 为家人 为梦想 为生存
[02:29.85]为了不再离开父母就身无分文
[02:32.58]拥有了它你对它绝对的信赖
[02:34.54]想当初 他们还没有进来
[02:36.48]你全身无力 活活像个病患
[02:38.24]任由世俗把病毒输入你的静脉
[02:40.43]教会你 如何不择手段
[02:42.52]你会因此跟你的梦想走散
[02:44.46]那不是你想要 你别为难
[02:46.41]不断往前走黑暗还没完
[02:48.42]你說過討厭現實勢利
[02:50.75]可是現在你討厭你自己
[02:53.12]你該有個信仰甚至對它也是
[02:56.17]失敗了算什麽大不了就多試幾次
[02:59.83]keep chase dream RMB會來的請相信
[03:04.32]過程裡是你留下的汗跟你的不信命[我說
[03:08.91]你該有個信仰甚至對它也是
[03:12.60]失敗了算什麽大不了就多試幾次
[03:16.45]keep chase dream RMB會來的請相信
[03:20.78]過程裡是你留下的汗跟你的不信命


31260600-Come Here RMB
Verse1:
他们就是几个数字
躺在你账户 让你度日
没了它 你寸步难行
更别想你要的hood dream
那时候你 还不知道
RMB 有多重要
直到开始 虚荣心围绕
需要自己解决暖饱
你hustle hustle到断了腿
违心话说到烂了嘴
觉得脑袋好像是灌了水
keep going 是为了谁
你稍微有点放松停下
包围你的就是生活廉价
是该一意孤行还是变的圆滑
他们说看 都是钱呐
come here RMB
u never know da how i need
有人靠它勉强维持生计
有人用它Light a weed
你說過討厭現實勢利
可是現在你討厭你自己
你該有個信仰甚至對它也是
失敗了算什麽大不了就多試幾次
keep chase dream RMB會來的請相信

你該有個信仰甚至對它也是
失敗了算什麽大不了就多試幾次
keep chase dream RMB會來的請相信
過程裡是你留下的汗跟你的不信命
Verse2：
如果要做就做next big
用你的夢想帶來RMB
请你脚踏实地 打破所有质疑
因为你想要的不止是那些纸币
赚到了money还要赚到了夸奖
给现实狠狠甩上一巴掌
跟现实对抗 到最后都是站着
也把它送给当初唱衰你的看客
把时间 都花在hustle里面
不断的赚钱不止为了活的体面
为自己 为家人 为梦想 为生存
为了不再离开父母就身无分文
拥有了它你对它绝对的信赖
想当初 他们还没有进来
你全身无力 活活像个病患
任由世俗把病毒输入你的静脉
教会你 如何不择手段
你会因此跟你的梦想走散
那不是你想要 你别为难
不断往前走黑暗还没完
你說過討厭現實勢利
可是現在你討厭你自己
你該有個信仰甚至對它也是
失敗了算什麽大不了就多試幾次
keep chase dream RMB會來的請相信
過程裡是你留下的汗跟你的不信命[我說
你該有個信仰甚至對它也是
失敗了算什麽大不了就多試幾次
keep chase dream RMB會來的請相信
過程裡是你留下的汗跟你的不信命
"""