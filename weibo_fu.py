from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from collections import Counter

# search keywords in weibo
search_kw = '伊朗'
# transfer the keywords into url code
kw_inurl = urllib.parse.quote(urllib.parse.quote(search_kw))

# complete the url address for searching
url_togo = 'https://s.weibo.com/weibo/{}?topnav=1&wvr=6&b=1'.format(kw_inurl)

# get your cookie from Chrome or Firefox
cookie = 'xxxxx'

# https headers including the cookies for logging in
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36',
    'cookie': cookie
}

# url request
req = urllib.request.Request(url_togo, headers=headers)
# open, read and decode
resp1 = urlopen(req).read().decode('utf-8')
# read with BeautifulSoup4
soup = BeautifulSoup(resp1, features='lxml')

search_limit = 40

# name of the weiboer
name = soup.find_all('a', 'name', limit=search_limit)
# content of this weibo
cont = soup.find_all('p', 'txt', limit=search_limit)
# number of likes this weibo get
like = soup.find_all(title='赞', limit=search_limit)
# forward = soup.find_all('a', attrs={'action-type': 'feed_list_comment'}, limit=search_limit)
# print(forward)

# combine three attrs
zip_content = zip(name, cont, like)
'''
# print seperately the contents of the weibo and their likes
for na, co, li in zip_content:
    print('\n', str.strip(na.get_text()))
    print(str.strip(co.get_text()))
    print('赞：', str.strip(li.get_text()))
    # print(str.strip(fw.get_text()))

for co in cont:
    print(str.strip(co.get_text()))
    seglist = jieba.cut(str.strip(co.get_text()))
    print('Default mode:', '，'.join(seglist))
'''
# list weibos in contents
contents = []
for co in cont:
    contents.append(str.strip(co.get_text()))
# combine weibos in contents
str = ''.join(contents)

# shows how many weibos searched at last
print('Searched for', len(contents), 'Weibos')
# list words in str
con_words = [word for word in jieba.cut(str) if len(word) >=2]
# print most common words with frequencies
print(Counter(con_words).most_common(15))

# generate wordcloud graph
# join the seperated words with spaces
new_text = ' '.join(con_words)
# define path for the font to be use in the wordcloud
font_path_mac = '/Users/.../STHeiti_Medium.ttc'
wordcloud_weibo = WordCloud(font_path=font_path_mac, width=1400, height=1000, margin=2).generate(new_text)
plt.imshow(wordcloud_weibo)
plt.axis('off')
plt.show()
