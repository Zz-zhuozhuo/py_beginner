"""
这是一个Python脚本，用于从Bilibili网站抓取”人工智能“专栏的视频信息。它使用了requests库来发送HTTP请求，并包含了必要的cookies和headers，以模拟浏览器行为
请务必控制请求频率，避免对Bilibili服务器造成过大压力
如果你需要使用这个脚本，请确保遵守Bilibili的使用条款和条件

出了这道门，以后不要供出为师的名字
（开玩笑的，不违法，不要恶意大量循环请求攻击就行
"""

# 不要忘了引入库，requests是用来发送网络请求的
import requests

# cookies一般是这个请求的必要部分，包含了用户的会话信息等，是由后端服务器规定的，一般用于验证请求的用户的身份
# 这里的cookies是从浏览器抓包得到的，可能会过期，需要定期更新（但至少我现在运行也没过期，说明这个cookie在一段时间内是有效的）
cookies = {
    'buvid_fp': '2ddfee00a1f905e6a06fcc9a4985d7af',
    'enable_web_push': 'DISABLE',
    'rpdid': "|(JYYku~m|)l0J'u~u)kl)ukY",
    'header_theme_version': 'CLOSE',
    'is-2022-channel': '1',
    'LIVE_BUVID': 'AUTO4817213891862473',
    'PVID': '1',
    'DedeUserID': '482876417',
    'DedeUserID__ckMd5': '7e5be7e58ecc6b84',
    'buvid4': '5CCC510C-2BA0-742E-5E7C-B15144457E3040154-024061305-7SmaxelINkpyatTScW%2FfwQ%3D%3D',
    'enable_feed_channel': 'ENABLE',
    'buvid3': '64F13DA3-A70E-E3DC-BAC3-F22C0493ABC557865infoc',
    'b_nut': '1749986757',
    '_uuid': 'D77E3C31-BF23-B88E-661D-35AFE102104FFD58207infoc',
    'bp_t_offset_482876417': '1079031024685416448',
    'b_lsid': '103110B3EA_197874A2C65',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTA1ODA2NzUsImlhdCI6MTc1MDMyMTQxNSwicGx0IjotMX0.V9nPlo_dZMXNQhoLSN4DpJK7E_VjdsS0yXWJeWRaWKk',
    'bili_ticket_expires': '1750580615',
    'SESSDATA': 'dd12df47%2C1765873475%2Cc0ac9%2A61CjB_y5gKemn7ClJPpxF-cLpm7qUNBHRukr1k-e0m_D37JyivmK_E6JCUmz6CWJKzYdMSVkJwZ0R0UVNDbm0tNXg1VS00SS1OYjhQek51R2E4dmNYMUtwTkdFT0JPSEtISThVRWZNSl92T3FpWUpfNkplY1VJSG45dHRxOTNmNVFZRk5qY09hS1dBIIEC',
    'bili_jct': '755358f395e6adcba13032a4bef56bdf',
    'CURRENT_FNVAL': '16',
    'sid': 'oqhy84eh',
    'home_feed_column': '5',
    'browser_resolution': '1571-807',
}

# headers是请求头，包含了浏览器信息、语言、缓存控制等，这些信息有助于服务器理解请求的来源和类型
# 同样，这些headers也是从浏览器抓包得到的，可能会过期或需要更新
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/',
    # 比如你看这里，浏览器信息是Google Chrome 137版本，Chromium 137版本，Not/A)Brand 24版本
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    # 比如你看这里，平台信息是macOS
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'cookie': "buvid_fp=2ddfee00a1f905e6a06fcc9a4985d7af; enable_web_push=DISABLE; rpdid=|(JYYku~m|)l0J'u~u)kl)ukY; header_theme_version=CLOSE; is-2022-channel=1; LIVE_BUVID=AUTO4817213891862473; PVID=1; DedeUserID=482876417; DedeUserID__ckMd5=7e5be7e58ecc6b84; buvid4=5CCC510C-2BA0-742E-5E7C-B15144457E3040154-024061305-7SmaxelINkpyatTScW%2FfwQ%3D%3D; enable_feed_channel=ENABLE; buvid3=64F13DA3-A70E-E3DC-BAC3-F22C0493ABC557865infoc; b_nut=1749986757; _uuid=D77E3C31-BF23-B88E-661D-35AFE102104FFD58207infoc; bp_t_offset_482876417=1079031024685416448; b_lsid=103110B3EA_197874A2C65; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTA1ODA2NzUsImlhdCI6MTc1MDMyMTQxNSwicGx0IjotMX0.V9nPlo_dZMXNQhoLSN4DpJK7E_VjdsS0yXWJeWRaWKk; bili_ticket_expires=1750580615; SESSDATA=dd12df47%2C1765873475%2Cc0ac9%2A61CjB_y5gKemn7ClJPpxF-cLpm7qUNBHRukr1k-e0m_D37JyivmK_E6JCUmz6CWJKzYdMSVkJwZ0R0UVNDbm0tNXg1VS00SS1OYjhQek51R2E4dmNYMUtwTkdFT0JPSEtISThVRWZNSl92T3FpWUpfNkplY1VJSG45dHRxOTNmNVFZRk5qY09hS1dBIIEC; bili_jct=755358f395e6adcba13032a4bef56bdf; CURRENT_FNVAL=16; sid=oqhy84eh; home_feed_column=5; browser_resolution=1571-807",
}

# 这里是请求的参数，包含了请求的具体内容，比如显示ID、请求数量、设备类型等
# 这些参数也是从浏览器抓包得到的，你可以改变这些参数来获取不同的内容
params = {
    'display_id': '1',
    # 比如，request_cnt是请求的数量，这里是15
    'request_cnt': '15',
    'from_region': '1011',
    'device': 'web',
    'plat': '30',
    'web_location': '333.40138',
    'w_rid': '18587a86562752d6898fe4a20568003c',
    'wts': '1750321548',
}

# 发送GET请求到Bilibili的API接口，获取“人工智能”推荐区域的内容
response = requests.get(
    'https://api.bilibili.com/x/web-interface/region/feed/rcmd',
    params=params,
    cookies=cookies,
    headers=headers,
)

# 打印响应的内容出来看一看，json你可以这么理解：在网络传输过程中，实际上传输的数据都是字典
# 只是把字典整个作为字符串来传输，这就是json，json本质上是个字符串
# 而对于请求返回的数据，.json()方法可以读取json字符串转为python的字典dict格式
print(response.json())

# 以下是解析响应内容，提取视频信息，并将其转换为DataFrame格式, 最终保存为Excel文件

# 首先安装和导入pandas库，这里的as的意思是重命名一下，之后我就直接可以用pd来代称
import pandas as pd

# 从响应中提取关键数据，其实是我print出来之后分析得到，我想要的关键信息在这里
data = response.json()['data']['archives']

# 创建一个列表来存储视频信息
df = pd.DataFrame(data)

# 保留bvid, title， duration, pubdate
df = df[['bvid', 'title', 'duration', 'pubdate']]

# 将pubdate转换为可读的日期格式
df['pubdate'] = pd.to_datetime(df['pubdate'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

# 将duration转换为分钟和秒的格式
df['duration'] = df['duration'].apply(lambda x: f"{x // 60}分{x % 60}秒")

# 将bvid转换为完整的视频链接，这里是我发现Bilibili的视频链接格式是这样的：https://www.bilibili.com/video/{bvid}
df['bvid'] = df['bvid'].apply(lambda x: f"https://www.bilibili.com/video/{x}")

# 最后将DataFrame保存为Excel文件，使用openpyxl引擎，openpyxl是一个处理Excel文件的库，也需要安装，pip install openpyxl
df.to_excel('bilibili_archives.xlsx',
            index=False, 
            header=['BVID', '标题', '时长', '发布时间'],
            engine='openpyxl')
