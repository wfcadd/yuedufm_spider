#Author:heming

import requests
from bs4 import BeautifulSoup
import re

class Fmspider(object):
    pg_list_all=[]
    pg_url_counter=74
    pg_url_page = "http://yuedu.fm/channel/1/"
    meta_info_list = []
    media_url = []
    # def __init__(self,baseurl,headers,cookies):
    #     self.baseurl=baseurl
    #     self.headers=headers
    #     self.cookies=cookies
    #     self.session=requests.session()
    #     self.session.headers=self.headers
    #     self.session.cookies.update(self.cookies)
    #     self.content_list=[]

    def __init__(self):
        # self.baseurl = baseurl
        pass


    def get_url_info(self,url):
        try:
            r = requests.get(url,timeout=3)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('error')



    #获得每个channel下一共有多少个分页,并返回所有分页的url列表
    def get_pg_split(self):

        base_url="http://yuedu.fm/channel/1/"
        for page in range(1,1000):
            html = self.get_url_info(Fmspider.pg_url_page)
            if html != 'error':
                soup = BeautifulSoup(html,"lxml")
                items = soup.find(text="下一页")
                if items == "下一页":
                    Fmspider.pg_list_all.append(Fmspider.pg_url_page)
                    Fmspider.pg_url_page=base_url+str(Fmspider.pg_url_counter)+'/'
                    Fmspider.pg_url_counter+=1
                    print('正在解析第{}页.....'.format(page))
                    print('第{}页解析完成!'.format(page))
                else:
                    print('正在解析第{}页.....'.format(page))
                    print('第{}页解析完成!'.format(page))
                    Fmspider.pg_list_all.append(Fmspider.pg_url_page)
                    Fmspider.pg_url_page=base_url+str(Fmspider.pg_url_counter)+'/'
                    print("一共{}页".format(page))
                    break

        return Fmspider.pg_list_all

    # 解析每页的链接内容,例如(url,imgurl,author,time,microphone)等等信息
    def Parse_item_info(self,url):
        html = self.get_url_info(url)
        base_url="http://yuedu.fm"
        author=''
        microphone_author=''
        publish_clock=''
        heardphones=''
        title=''
        channel_article_url=''
        channel_article_img_url=''
        channel_article_description=''
        if html != 'error':
            soup1 = BeautifulSoup(html,"lxml")

            #对当前访问的页面获取所有分页链接并存放在数组中,pg_split接受一个BeautifulSoup对象作为参数
            # pglist=self.pg_split(soup1)
            # print(pglist)


            items = soup1.find('div',class_='wp fl')
            # print(items)
            for item in items.find_all('li'):

                # print(item.find('div',class_="channel-pic fl"))
                # print(item.div.a['href'])
                # print(item.div.a)


                # 获取文章url
                access_path=item.find('div',class_="channel-pic fl")
                # print(access_path.a['href'])
                channel_article_url=base_url+access_path.a['href']

                # 获取img url
                # print(access_path.a.img['src'])
                channel_article_img_url=base_url+access_path.a.img['src']


                # 获取article description
                access_channel_article_desc = item.find('div',class_='channel-desc')
                channel_article_description=access_channel_article_desc.string
                # print(channel_article_description)

                # 获取文章标题
                find_article_title = item.find('div',class_="channel-title")
                # print(find_article_title)
                title = find_article_title.a.string
                # print(article_title)

                # 获取meta信息
                channel_meta_info = item.find('div',class_="channel-meta")
                for l in channel_meta_info.find_all('span'):
                    # print(l.i.attrs)
                    if l.i.attrs['class'][0]=='fa' and l.i.attrs['class'][1]=='fa-pencil':
                        # print(l.contents[1])
                        author=l.contents[1]
                        # print(author)
                    if l.i.attrs['class'][0]=='fa' and l.i.attrs['class'][1]=='fa-microphone':
                        # print(l.contents[1])
                        microphone_author=l.contents[1]
                    if l.i.attrs['class'][0]=='fa' and l.i.attrs['class'][1]=='fa-clock-o':
                        # print(l.contents[1])
                        publish_clock=l.contents[1]
                    if l.i.attrs['class'][0]=='fa' and l.i.attrs['class'][1]=='fa-headphones':
                        # print(l.contents[1])
                        heardphones=l.contents[1]
                        # print(heardphones)


                Fmspider.meta_info_list.append({'article_title':title,'article_url':channel_article_url,'img_url':channel_article_img_url,'article_desc':channel_article_description,'meta_data':{'fm_author':author,'fm_microphone_author':microphone_author,'fm_publish_time':publish_clock,'fm_heardphones':heardphones}})
            # 将meta_info_list配置为全局变量,并进行返回
            return Fmspider.meta_info_list



    # pg_pattern = selector.xpath('//div[@class="wp fl"]/div[@class="pg"]/a/text()')
    def parse_video_url(self,url,article_title):
        html = self.get_url_info(url)

        if html != 'error':
            soup = BeautifulSoup(html,'lxml')
            items = soup.find(text=re.compile('(\w+).mp3'))
            Fmspider.media_url.append({'article_title':article_title,'media_url':'http://yuedu.fm'+items[230:283]})

        return Fmspider.media_url


    def url_combination(self):
        """combine the url """
        pass





if __name__=='__main__':
    # url = "http://yuedu.fm/1/1025/"
    fm = Fmspider()
    #解析一共有多少个分页,返回一个分页列表,并赋值给p
    p=fm.get_pg_split()
    # print(p)
    #遍历分页列表,并将ip传入到Parse_item_info来解析所有分页中的所有url地址及一些meta信息,返回信息列表赋值给info_list变量
    for i in p:
        info_list = fm.Parse_item_info(i)


    print('本栏目中所有分页的fm信息列表为:{}'.format(info_list))
    #遍历上一步返回的info_list变量,并传入article_url和article_title参数到parse_video_url方法来解析播放url并返回列表赋值给video_list
    for m in info_list:
        # print(m['article_title'],m['article_url'])
        video_list = fm.parse_video_url(m['article_url'],m['article_title'])
        print('正在解析fm播放URL列表..............')
    print('fm播放url列表解析完成!')
    print('fm播放url列表为:{}'.format(video_list))



