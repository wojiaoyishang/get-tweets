from flask import Flask, request
import threading
import requests
import base64
import time

app = Flask(__name__)

# 代理地址
PROXIES = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 是否 SSL 验证
SSL_VER = False

# 禁用掉警告
requests.packages.urllib3.disable_warnings()

# 图片队列
illustrations = []

def save_illustration(src: str):
    """保存文件到目录

    Args:
        src (str): 要下载文件的网址
    """
    # 处理保存的文件名
    pos = src.rfind("?")
    pos = len(src) if pos == -1 else pos  # 这两行代码来找问号的位置
    saveFileName = src[src.rfind("/") + 1:pos] + ".jpg" # 取出文件名
    
    response = requests.get(src, stream=True, proxies=PROXIES, verify=SSL_VER)
    # content_size = int(response.headers['content-length'])  # 内容体总大小
    file_size = 0

    with open(f"images/{saveFileName}", "wb") as f:
        for data in response.iter_content(1024 * 5):
            f.write(data)
            file_size += len(data)
            #print(
            #   f"\r正在下载图片 {saveFileName} ，进度：{file_size}B / {content_size}B - {round(file_size / content_size * 100, 2)}%",
            #    end="")

    print(f"\n下载图片 {saveFileName} 完成！")
    response.close()
    
def download_master():
    """用来处理插画的队列的"""
    print("已经开始图片下载队列......")
    while True:
        time.sleep(0.5)
        if len(illustrations) != 0:
            print("开始下载图片", illustrations[0])
            save_illustration(illustrations[0])
            illustrations.pop(0)

@app.route("/")
def api():
    # 获取发过来的插画链接
    url = request.args.get("url", None)
    if url is None:
        return {"msg": "no url."}
    
    url = base64.b64decode(url).decode() # base64解码
    print("获取到图片链接", url)    
    illustrations.append(url)
    
    return {"msg": "success"}
    
if __name__ == "__main__":
    threading.Thread(target=download_master).start()
    app.run()