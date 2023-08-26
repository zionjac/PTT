import requests,time
from bs4 import BeautifulSoup
pttstocks=[]
URL = 'https://www.ptt.cc/bbs/Stock/index.html'
urls=[]
def parse(url):
    rc = requests.get(url)
    if rc.status_code ==200:
        spc = BeautifulSoup(rc.text, 'lxml')
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
t1 = time.time()
for url in urls:
    parse(url)
print("Normal total time:", time.time()-t1)
