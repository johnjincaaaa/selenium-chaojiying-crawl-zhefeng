import requests
from fake_useragent import FakeUserAgent
from lxml import etree
import pymongo

def windows_pictures(pages,mongodb_ip):
    """
    获取电脑壁纸的页面地址，并存入mongodb
    :param pages: 总页数
    :param mongodb_ip: mongodb的ip
    :return:
    """
    client = pymongo.MongoClient(mongodb_ip)
    db = client['哲风壁纸']
    collection = db['解析图片']



    headers = {'user-agent':FakeUserAgent().random}

    for i in range(pages):

        resp = requests.get(url=f'https://haowallpaper.com/homeView?isSel=false&page={i}',headers=headers)
        # print(resp.status_code,resp.text)
        tree = etree.HTML(resp.text)
        urls = tree.xpath('//div[@class="card--button"]/a/@href')
        titles = tree.xpath('//div[@class="card"]/img/@title')
        data = [{'urls':'https://haowallpaper.com/'+i,'titles':j}for i,j in zip(urls,titles)]
        print(data)
        collection.insert_many(data)

if __name__ == '__main__':

    windows_pictures(2,'mongodb://127.0.0.1:27017')

