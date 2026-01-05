import requests
cookies = {    
'll': '"118172"',    
'bid': '1g9KuH68SK4',    
'_pk_id.100001.4cf6': 'b0cd6adabb706ae6.1718802720.',    
'__yadk_uid': '7Fy28aQx1DCY4NnZHNsGL18fq4eCFizJ',    
'__utmc': '30149280',    
'__utmz': '30149280.1718802721.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',    
'__utmc': '223695111',    
'__utmz': '223695111.1718802721.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',    
'_vwo_uuid_v2': 'D816E9B77293C40EA8C8478097A9394E6|8963e2d5854837c41641bb0564b6793f',    
'_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1718810576%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DI5UDdlLzyTcOQNcMLaeu6-ehnN7_hAH4R1JwYjyyLmFkXPGCnNdtD8MKfk52YKMgSTO_ecVUL9Drv0n-aGmR2q%26wd%3D%26eqid%3De79e93560000072c000000046672d91c%22%5D',    
'_pk_ses.100001.4cf6': '1',    
'ap_v': '0,6.0',    
'__utma': '30149280.23331474.1718455367.1718802721.1718810577.3',    
'__utma': '223695111.1593040718.1718802721.1718802721.1718810577.2',    
'__utmb': '223695111.0.10.1718810577',    
'__utmt': '1',    
'__utmb': '30149280.1.10.1718810577',
}
headers = {    
'accept': '*/*',    
'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',    
'cache-control': 'no-cache',    
# 'cookie': 'll="118172"; bid=1g9KuH68SK4; _pk_id.100001.4cf6=b0cd6adabb706ae6.1718802720.; __yadk_uid=7Fy28aQx1DCY4NnZHNsGL18fq4eCFizJ; __utmc=30149280; __utmz=30149280.1718802721.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1718802721.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _vwo_uuid_v2=D816E9B77293C40EA8C8478097A9394E6|8963e2d5854837c41641bb0564b6793f; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1718810576%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DI5UDdlLzyTcOQNcMLaeu6-ehnN7_hAH4R1JwYjyyLmFkXPGCnNdtD8MKfk52YKMgSTO_ecVUL9Drv0n-aGmR2q%26wd%3D%26eqid%3De79e93560000072c000000046672d91c%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.23331474.1718455367.1718802721.1718810577.3; __utma=223695111.1593040718.1718802721.1718802721.1718810577.2; __utmb=223695111.0.10.1718810577; __utmt=1; __utmb=30149280.1.10.1718810577',    
'pragma': 'no-cache',    
'priority': 'u=1, i',    
'referer': 'https://movie.douban.com/',    
'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',    
'sec-ch-ua-mobile': '?0',    
'sec-ch-ua-platform': '"macOS"',    
'sec-fetch-dest': 'empty',    
'sec-fetch-mode': 'cors',    
'sec-fetch-site': 'same-origin',    
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',    
'x-requested-with': 'XMLHttpRequest',
}
params = {    
'type': 'movie',    
'tag': '热门',    
'page_limit': '100',    
'page_start': '0',
}
response = requests.get('https://movie.douban.com/j/search_subjects', params=params, cookies=cookies, headers=headers)
# movie_dict结果数据
movie_dict = response.json()
"""""
movies = movie_dict['subjects'][:100]
cover_img_name_list = []
set_1=set()  # 限制为100条数据
for movie in movies:
    f_url=movie.get('cover', '')
    if f_url:
       f_jpg=f_url.split('/')[-1]
       if f_jpg not in set_1:
          set_1.add(f_jpg)
          cover_img_name_list.append(f_jpg)
print(cover_img_name_list)
"""""
movies = movie_dict['subjects']
new_list = []
for movie in movies:
    f_1=movie.get('title', '')
    f_2=movie.get('rate', '')
    f_3=movie.get('is_new', False)
    if len(f_1)<=4 or f_3==True or float(f_2)>=8 and f_3==False:
       new_list.append(movie)
new_dict={}
for movie in new_list:
    movie_id=movie['id']
    movie_info={
        key:value for key,value in movie.items()
        if key!='id'
    }
new_dict[movie_id]=movie_info
print(new_dict)