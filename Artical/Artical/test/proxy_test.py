import requests


headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
}
# url = 'https://www.baidu.com/'
url = 'https://www.google.com/'
# url = 'http://blog.jobbole.com/114473/'
proxy = {

    # 'http':'122.241.72.32:808'
    'http':'69.85.195.148:60736'
}
response = requests.get(url=url,headers=headers,proxies=proxy)
print(response.text)
print(response.status_code)

# 测试结果：访问伯乐在线的代理ip，需要http协议，80端口
































































