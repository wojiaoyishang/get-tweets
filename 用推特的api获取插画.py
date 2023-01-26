import requests, time

# ------ 定义请求时的必要参数 ------

# 代理地址
PROXIES = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 是否 SSL 验证
SSL_VER = False

# 禁用掉警告
requests.packages.urllib3.disable_warnings()

# 请求头
REQUEST_HEADER =  {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
  'Accept': '*/*',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'x-guest-token': '',
  'x-twitter-client-language': 'zh-cn',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
  'Referer': 'https://twitter.com/',
  'Connection': 'keep-alive'
}


def save_illustration(src: str):
    """保存文件到目录

    Args:
        src (str): 要下载文件的网址
    """
    # 处理保存的文件名
    pos = src.rfind("?")
    pos = len(src) if pos == -1 else pos  # 这两行代码来找问号的位置
    saveFileName = src[src.rfind("/") + 1:pos] # 取出文件名
    
    response = requests.get(src, stream=True, proxies=PROXIES, verify=SSL_VER)
    content_size = int(response.headers['content-length'])  # 内容体总大小
    file_size = 0

    with open(f"images/{saveFileName}", "wb") as f:
        for data in response.iter_content(1024 * 5):
            f.write(data)
            file_size += len(data)
            print(
                f"\r正在下载图片 {saveFileName} ，进度：{file_size}B / {content_size}B - {round(file_size / content_size * 100, 2)}%",
                end="")

    print(f"\n下载图片 {saveFileName} 完成！")
    response.close()


# save_illustration("https://pbs.twimg.com/media/FmrMe2cacAIQUL8?format=jpg&name=large")  # 测试图片下载

# 获取访客 token
result = requests.post("https://api.twitter.com/1.1/guest/activate.json", headers=REQUEST_HEADER, proxies=PROXIES, verify=SSL_VER).json()
REQUEST_HEADER['x-guest-token'] = result['guest_token']
print("Guest_Token:", result['guest_token'])

# 获取推文
tweets = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?"
                        "screen_name=mafumuffin&"
                        "include_rts=false&"
                        "exclude_replies=true&"
                        "count=200", headers=REQUEST_HEADER, proxies=PROXIES, verify=SSL_VER).json()
while True:
    print("---休息5s---")
    time.sleep(5)
    if len(tweets) - 1 == 0:
        times = 1
    else:
        times = len(tweets) - 1
        
    for i in range(times):  # 遍历少一条推文，便于我们连续获取。少这一条推文会在下一次获取补上。
        tweet = tweets[i]    

        print("此条推文发布时间：", tweet['created_at'])
        print("此条推文ID：", tweet['id_str'])
        print("此条推文内容：", tweet['text'])
        if 'media' not in tweet['entities']:
            print("此条推文携带的附件：无\n", end="")
            print("-"*100)
            continue
        print("此条推文携带的附件：\n", end="")
        for medium in tweet['extended_entities']['media']:
            print(f"{medium['media_url']}")
            if medium['type'] == 'photo':
                for size in medium['sizes'].keys():
                    if size == "large":
                        print(f"找到资源 {size}: {medium['media_url']}?format=jpg&name={size}")
                        save_illustration(f"{medium['media_url']}?format=jpg&name={size}")
                    
        print("-"*100)
    
    if len(tweets) - 1 == 0:
        break  # 全部获取完毕
    else:
        tweets = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?"
                        "screen_name=mafumuffin&"
                        "include_rts=false&"
                        "exclude_replies=true&"
                        "count=200&"
                        "max_id=" + tweets[i + 1]['id_str'], headers=REQUEST_HEADER, proxies=PROXIES, verify=SSL_VER).json()

    
