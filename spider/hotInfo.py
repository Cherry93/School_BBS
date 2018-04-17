import requests
from lxml import etree
import json
url = 'http://yz.chsi.com.cn/kyzx/kydt/'  # 目标网址
page = requests.get(url)    # 获取网页对象

sector = etree.HTML(page.text)  # html解析
info = sector.xpath('//div[@class="content-l"]/ul/li/a//text()')    # 查找标题
link = sector.xpath('//div[@class="content-l"]/ul/li/a/@href')      # 对应的链接
base_url= 'http://yz.chsi.com.cn'
target_link = []    # 我们需要的网址信息
for i in link:
    res = base_url+i
    target_link.append(res)
print(target_link)

### 转化json 存到数据库
res=[dict(title=info[index], link=target_link[index]) for index in range(len(info))]
print(res)
res2 = [dict(model = 'hotinfo.hotinfo',fields = k) for k in res]
print(res2)

# json_str2 = json.dumps(res2,ensure_ascii=False)
# print ("python原始数据：", repr(res2))
# print ("json对象：", json_str2,type(json_str2))

with open("./bbstest.json",'w',encoding='utf-8') as json_file:
     json.dump(res2,json_file,ensure_ascii=False)