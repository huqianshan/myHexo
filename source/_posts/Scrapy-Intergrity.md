---
layout: poster
title: Scrapy Intergrity
date: 2019-01-16 20:49:22
tags: [python]
---
# THE COLLECTION OF SCRAPY PYTHON SCRIPTS
<!--more-->
***
 1. 爬取留学网站的相关信息 
    ```python
    import requests
    import os
    from bs4 import BeautifulSoup
    import urllib

    def find_page_link(dic,soup):
     for link in soup.findAll(class_='news-title'):
    #获取h4的子tag a
         aLink=link.a
    # 获取 a 中的href
         hrefLink=aLink.get('href')
         titleLink=aLink.get('title')
         dic[titleLink]=hrefLink

    def save_to_file(file_name, contents):
        fh = open(file_name, 'w')
        fh.write(contents)
        fh.close()


    def Schedule(a,b,c):
      per = 100.0 * a * b / c
         if per > 100 :
             per = 100
      print('%.2f%%' % per)

    def save_img(img_url,file_name,file_path='D:\Data\File\sky'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print('文件夹',file_path,'不存在，重新建立')
            os.makedirs(file_path)
        #获得图片后缀
        file_suffix = os.path.splitext(img_url)[1]
        #拼接图片名（包含路径）
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,'.jpg')
       #下载图片，并保存到文件夹中
        #create the object, assign it to a variable
        proxy = urllib.request.ProxyHandler({"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"})
        # construct a new opener using your proxy settings
        opener = urllib.request.build_opener(proxy)
        opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
        ]
        urllib.request.install_opener(opener)
        try: 
            urllib.request.urlretrieve(img_url,filename,Schedule)
        except Exception as e:
            print('图片下载时发生错误 ：',e)
    except IOError as e:
        print('文件操作失败',e)
    except Exception as e:
        print('错误 ：',e)


    dic={}
    for num in range(2,11):
    prefix='https://www.liuxue86.com/news/liuxuexinwen/'
    link=prefix+str(num)+'.html'
    #获取html 文件
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
        Html=requests.get(link,headers)
        soup=BeautifulSoup(Html.content,'html.parser')
    #找到新闻链接
        find_page_link(dic,soup)
    except Exception as err:
        print(err)
    finally:
        Html.close()
    #提取主页面中链接，字典存储标题，链接
    
    #
    ```
 2. 爬取大众点评网的商家信息

```python
    def get_user_agent():
         user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        ]
        return random.choice(user_agent)


def save_to_txt(file_name,dic):
    with open(file_name,'a+',encoding='utf-8') as file:
        for key,value in dic.items():
            file.write(key+":"+value)
            file.write('\n')
        file.close()
    print("fined writing\n\r")
        
def find_hotel_url(soup):
    dic={}
    link_prefix='https://www.dianping.com/shop/'
    # the divs that store the hotel name and link
    body=soup.findAll('li',class_='hotel-block')    
    for tem in body:
        name=tem.a.get_text()
        num=tem['data-poi']
        link=link_prefix+num
        dic[name]=link
    return dic

    """
get hotel's link of chengdu city
radomly choose user_agent
input: 
    fp: begin page
    tp: end page
    (default in function : href)
 return :
     dic : keyvalue(hotelname),key(hotel url)
"""
def scrapy_link_main(fp,tp):
    for i in range(fp,tp+1):
        # initialize url with prefix and suffix
        href_prefix="https://www.dianping.com/chengdu/hotel/"
        href_suffix="p"+str(i)       
        if i == 0:
            href_suffix="p"
        href=href_prefix+href_suffix
        
        headers = {'User-Agent': get_user_agent()}
        Html=requests.get(href,headers=headers)
        soup=BeautifulSoup(Html.content,'html.parser')   
        print(soup.ROOT_TAG_NAME)
        soup.name
        # store {Hotel_name: link} in to txt in dictionary type
        
        dic=find_hotel_url(soup)
        
        print(dic)  
        filename='.\hotel\hotel_url.txt' 
        
        save_to_txt(filename,dic)

        # scrap information and store it 
"""
input: none
output: txt
"""
def txt_to_dic():
    filename='.\hotel\hotel_url.txt'
    dic={}
    with open(filename,'r',encoding='utf-8') as file:
            for line in file:
                #print(line, end='')
                tem=line.split(':',maxsplit=1)
                dic[str(tem[0])]=str(tem[1])
    print('Txt loads fine')
    print("dic has %s "%(len(dic)))
    return dic 

def get_soup(name,url):
    hotel_link=url
    # need Cookie to get avoid of checking
    headers = {'User-Agent': get_user_agent(),
               'Cookie':'__mta=150787721.1541145960944.1541166756059.1541208492067.12; cy=8; cye=chengdu; _lxsdk_cuid=166d3570de5c8-07985b70746ce-b79183d-144000-166d3570de69d; _lxsdk=166d3570de5c8-07985b70746ce-b79183d-144000-166d3570de69d; _hc.v=c746c1d8-9fb6-4e00-2712-20e2880ac118.1541143993; s_ViewType=10; cityInfo=%7B%22cityId%22%3A8%2C%22cityEnName%22%3A%22chengdu%22%2C%22cityName%22%3A%22%E6%88%90%E9%83%BD%22%7D; __utma=1.1900410642.1541164771.1541164771.1541164771.1; __utmz=1.1541164771.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=166d72f44b8-8f2-afd-052%7C%7C2'
          }
    
    try :      #s=requests.Session()
        Html=requests.get(hotel_link,headers=headers)
        status_code=Html.status_code
        # may url error(404) or the ip is forbidden by the server(404)
        # it needs  to checking by hands    
        if status_code!=200:
            print("Name:%s Url: %s ----Response error! %s"%(name,url,status_code))
            time.sleep(random.randint(1,3))
            return None
        # some other exception caused by potential mistakes
    except Exception as ex:
        time.sleep(random.randint(1,5))
        print('Connect Error---- %s -----%s'%(name,url))
        print(ex)
        return None
    
    print("Hotel %s  link %s : Response Code is : %s \n ! "%(name,url,Html))
    # Use BeautiofulSoap to analysize html file
    soup=BeautifulSoup(Html.content)
    
    # after some scraping The server may need Verification Code
    # the captcha page's reponse is also 200,but the title is "验证中心"
    tit=soup.find('title').get_text()
    if tit=="验证中心":
        print('---Sorry  Need to get out of Verification Manually----')
        while True:
            print(' Enter goon to Continue ')
            g=input()
            if g=='goon':
                break
                
    #print(Html.headers)    
    Html.close()
    time.sleep(random.randint(1,3))    
    #print("Print Response main Body \n %s"%(soup.contents))
    return soup


def get_information(soup):
    # get phone_number (t) and address(a)
    t=soup.find('div',class_='info-value')
    #print("phone number is %s\n"%(t))
    a=soup.find('span',class_='hotel-address')
    #print('hotel number is %s\n'%(a))
    
    # it may cannot find the phone div or address
    # thus will throw a exception
    try:
        phone_num=t.get_text()        
    except Exception as ex:
        print(" %s Get information failed Maybe PhoneNum lost;"%(ex)) 
        phone_num="None"        
    try:
        address=a.get_text()
    except Exception as ex:
        print(" %s Get information failed Maybe Address lost;"%(ex)) 
        address='None'
        
    return [phone_num,address] 

def write_to_json(dic):
    with open('data.json', 'w',encoding='utf-8') as f:
        # for Chinese tyoe text's json storing ,it must set the 
        # ensure_ascii False
        dic_json=json.dumps(dic,indent=4,ensure_ascii=False)
        f.write(dic_json)

def information_scrap():
    # get url dic
    dic=txt_to_dic()
    
    # make a dic(json like) to store 
    dic_json={}
    i=0
       
    #get url  loop,
    for name,link in dic.items():
        link=link[:-1]
        soup=get_soup(name,link)
        i+=1
        print(i)
        
        # when url is False or Connection Failed the return soup is None
        if not soup:
            print("the url is broken Continue Next")
            continue
        
        [ph,add]=get_information(soup)
        
        # the link,phone,address is saved in  [list]
        sub_dic=[link,ph,add]
        print(sub_dic)
        dic_json[name]=sub_dic
    return dic_json 
```