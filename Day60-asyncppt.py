import aiohttp, asyncio
import requests, time
from bs4 import BeautifulSoup
pttstocks=[]
urls=[]
URL = 'https://www.ptt.cc/bbs/Stock/index.html'
n=4 #可自訂
for i in range(n):
    print(f"第 {i+1} 頁")
    r = requests.get(URL)
    sp = BeautifulSoup(r.text, 'lxml')
    datas = sp.find_all("div", class_='r-ent')#datas有該網頁文帖的標題和相對網址
    for data in datas:
        if data.a:
            urlc ='https://www.ptt.cc' + data.a.get('href')
            urls.append(urlc)
    if sp.find(class_='btn wide disabled')=='‹ 上頁':
        break
    else:
        URL ='https://www.ptt.cc' + sp.find_all('a', class_='btn wide')[1].get('href')

print(f'爬取{n}頁,{len(urls)}篇文章')


async def fetch(session, url):
    async with session.get(url) as response:
        html = await response.text()
        parsed_data = parse(html)  # 使用自定义的 parse() 函数处理 HTML 内容
        return parsed_data

async def main():
    global urls
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        #print(results)
def parse(html):
    spc = BeautifulSoup(html, 'lxml')
    main_container = spc.find(id='main-container')
    all_text = main_container.text
    if '\n--\n' in all_text:
        cont_text = all_text.split('\n--\n')[0]
    else: 
        cont_text = all_text.split('\n※ ')[0]
    contlist = cont_text.split('\n')
    while '' in contlist:
        contlist.remove('')
    pttstocks.append(contlist)


t1=time.time()    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
print("Async total time:", time.time()-t1)
with open('stock_news.txt', 'a',encoding='utf8') as f:
    for ptts in pttstocks:
        print('\n'.join(ptts),file=f)
        print('-'*100,file=f)