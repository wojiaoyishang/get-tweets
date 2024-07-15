# 批量获取推文

#### 介绍

> **⚠️注意** 由于更新了通过 Python + Playwright 获取推文的方法，故把不同代码放入了两个不同的文件夹内，

| 爬取方式                     |                                                                          链接                                                                          |                                             视频说明                                             |
|:-------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------:|
| Python + Playwright （推荐） |                            [点我前往](https://gitee.com/wojiaoyishang/get-tweets/tree/master/Playwright%20%E6%96%B9%E6%B3%95)                            | [https://www.bilibili.com/video/BV1mx4y1t7Uo](https://www.bilibili.com/video/BV1mx4y1t7Uo/) |
| 油猴脚本 + Python下载          | [点我前往](https://gitee.com/wojiaoyishang/get-tweets/tree/master/%E6%B2%B9%E7%8C%B4%E8%84%9A%E6%9C%AC%20+%20Python%E8%81%94%E5%8A%A8%E6%96%B9%E6%B3%95) |  [https://www.bilibili.com/video/BV1M34y1f7oz](https://www.bilibili.com/video/BV1M34y1f7oz)  

#### Python + Playwright

+ main.py -- 主要文件
+ images -- 保存图片文件夹（会自动创建）
+ cookies.json -- 推特有效的 Cookie ，需要自行修改

> **⚠️注意** 请先安装依赖！

+ httpx  -- 异步请求库
+ bs4  -- BeautifulSoup 格式化
+ lxml  --  网页解析器
+ playwright  --  操作浏览器

#### 油猴脚本 + Python下载

+ images -- 文件夹，保存插画的文件夹，**一定要预先创建**
+ main.py -- Python代码
+ Tampermonkey -- 外部引用方式.js -- 文件引入方式
+ Tampermonkey -- 直接粘贴到 Tampermonkey 中即可.js -- 直接调用方式（二者选择其一即可）
+ 用推特的api获取插画.py -- 访客 API 获取插画示例
