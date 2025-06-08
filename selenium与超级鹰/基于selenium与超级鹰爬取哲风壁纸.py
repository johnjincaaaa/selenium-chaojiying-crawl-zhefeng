
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium与超级鹰.chaojiying import Chaojiying_Client
from PIL import Image,ImageDraw
from time import sleep

# 实例化Options对象来关闭自动化特性
options = Options()
# 使用Options关闭自动化扩展，防止被检测到是使用其他工具驱动的浏览器
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 使用add_argument禁用浏览器自动化特性，防止被检测到是使用其他工具驱动的浏览器
options.add_argument('--disable-blink-features=AutomationControlled')
# 忽略证书错误，防止因为证书错误导致访问失败
# options.add_argument('ignore-certificate-errors')



def get_url_list(page:int):
    """
    得到每一页的图片地址
    :param page: 第几页
    :return: url列表
    """
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://haowallpaper.com/?isSel=false&page={page}')
    driver.maximize_window()
    img_elements = driver.find_elements(By.XPATH,'//div[@class="card--button"]/a')
    return [i_.get_attribute('href') for i_ in img_elements]

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

    img_element.screenshot('parsing_picture.png')
    width = img_element.size.get('width')
    # 实例化超级鹰api返回坐标
    image = open('parsing_picture.png', 'rb').read()
    chao = Chaojiying_Client('johnjincaaaa', 'wodianhua1', '969453')
    position:str = chao.PostPic(image,9901)['pic_str']
    print(position)
    x = int(position.split(',')[0])
    y = int(position.split(',')[1])
    # 画图检查超级鹰返回坐标点
    image1 = Image.open('parsing_picture.png')
    draw = ImageDraw.Draw(image1)
    draw.ellipse((x-3,y-3,x+3,y+3),fill='red')
    image1.save('parsing_dot.png')


    # 创建动作链并移动小滑块113,122
    action = webdriver.ActionChains(driver)
    slider = driver.find_element(By.XPATH,'//div[@class="slider-bar"]/input')
    action.click_and_hold(slider)
    action.move_by_offset(x-width//2,0).perform()
    action.release(slider).perform()
    sleep(2)


if __name__ == '__main__':
    pages = int(input('你想爬取多少页:'))
    for i in range(pages):
        urls = get_url_list(i)
        for j in urls:
            parse_single_url(j)