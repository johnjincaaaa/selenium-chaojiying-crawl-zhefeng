from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from 自动化工具与超级鹰.chaojiying import Chaojiying_Client
from PIL import Image,ImageDraw
from time import sleep
import pymongo
import os
# 实例化Options对象来关闭自动化特性
options = Options()
# 使用Options关闭自动化扩展，防止被检测到是使用其他工具驱动的浏览器
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 使用add_argument禁用浏览器自动化特性，防止被检测到是使用其他工具驱动的浏览器
options.add_argument('--disable-blink-features=AutomationControlled')
# 忽略证书错误，防止因为证书错误导致访问失败
options.add_argument('ignore-certificate-errors')
# 配置下载路径
download_path = os.path.abspath('downloaded')  # 替换为实际路径
options.add_experimental_option('prefs', {
    'download.default_directory': download_path,
    'download.prompt_for_download': False,  # 禁止弹出下载确认对话框
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})


def parse_single_url(url:str):
    """
    解析爬取规则
    :param url: 图片网页
    :return:
    """
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()
    driver.find_element(By.XPATH,'//div[@class="hao-bottom-nav-end DownButtom"]/span').click()
    sleep(1)
    img_element = driver.find_element(By.XPATH,'//div[@class="captcha-images"]/img[1]')
    signal = url.split('/')[-1]
    img_element.screenshot(f'picture/{signal}parsing_picture.png')
    width = img_element.size.get('width')

    # 实例化超级鹰api返回坐标
    image = open(f'picture/{signal}parsing_picture.png', 'rb').read()

    """
    这里设置你的超级鹰账号和密码
    """
    chao = Chaojiying_Client('', '', '969453')
    position:str = chao.PostPic(image,9901)['pic_str']
    print(position)
    x = int(position.split(',')[0])
    y = int(position.split(',')[1])

    # 画图检查超级鹰返回坐标点
    image1 = Image.open(f'picture/{signal}parsing_picture.png')
    draw = ImageDraw.Draw(image1)
    draw.ellipse((x-3,y-3,x+3,y+3),fill='red')
    image1.save(f'picture/{signal}parsing_dot.png')


    # 创建动作链并移动小滑块113,122
    action = webdriver.ActionChains(driver)
    slider = driver.find_element(By.XPATH,'//div[@class="slider-bar"]/input')
    action.click_and_hold(slider)
    action.move_by_offset(x-width//2,0).perform()
    action.release(slider).perform()
    sleep(5)
    driver.close()

def link_mongodb_to_get_url(mongodb_ip,title):
    """
    连接到mongodb获取地址并解析
    :param mongodb_ip:
    :param title: 需要下载的图片名称
    :return:
    """
    client = pymongo.MongoClient(mongodb_ip)
    db = client['哲风壁纸']
    collection = db['解析图片']
    data = collection.find({'titles':{'$regex':title}})
    if data:
        print(f'搜索到关键词{title},数据库有以下图片信息：')
        for i in data:
            print(i)
            parse_single_url(i.get('urls'))
            print('下载成功！！')
    else:
        print(f'数据库没有关键词为{title}的信息')

if __name__ == '__main__':
    title = input('你想下载的图片名字：')
    link_mongodb_to_get_url('mongodb://127.0.0.1:27017',title)