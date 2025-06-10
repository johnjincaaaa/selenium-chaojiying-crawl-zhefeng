
# 哲风壁纸爬取工具  

该项目用于爬取 [哲风壁纸](https://haowallpaper.com/) 的壁纸资源，包含页面链接采集、验证码识别与图片下载功能，依赖 MongoDB 存储中间数据。


## 一、项目功能概述  
1. **页面链接采集**：`each_url_getting.py` 脚本通过请求页面列表页，提取壁纸详情页链接和标题，存储到 MongoDB。  
2. **图片下载**：`基于selenium与超级鹰爬取哲风壁纸.py` 脚本从 MongoDB 读取目标壁纸链接，使用 Selenium 模拟浏览器访问，通过超级鹰平台识别验证码（滑动验证坐标），完成下载。  
3. **验证码识别**：`chaojiying.py` 是超级鹰验证码识别的官方客户端，用于调用验证码识别接口。  


## 二、环境与依赖  
### 1. 环境要求  
- Python 3.7+  
- MongoDB（需提前安装并启动服务）  
- Chrome 浏览器（需匹配 Selenium 使用的 ChromeDriver 版本）  

### 2. 依赖库安装  
```bash
pip install requests fake_useragent lxml pymongo selenium Pillow
```


## 三、项目结构  
```
自动化工具与超级鹰/
├── each_url_getting.py        # 采集壁纸详情页链接，存储到 MongoDB
├── 基于selenium与超级鹰爬取哲风壁纸.py  # 从 MongoDB 读取链接，完成验证码识别与图片下载
├── chaojiying.py              # 超级鹰验证码识别客户端
├── picture/                   # 临时存储验证码截图及标注点（需手动创建）
└── downloaded/                # 图片下载目录（需手动创建）
```


## 四、使用步骤  

### 1. 配置准备  
- **MongoDB 连接**：确保 MongoDB 服务已启动，默认连接地址为 `mongodb://127.0.0.1:27017`（可在代码中修改）。  
- **超级鹰账号**：注册 [超级鹰](http://www.chaojiying.com/) 账号，获取用户名、密码和软件 ID（`soft_id`），并在 `基于selenium与超级鹰爬取哲风壁纸.py` 中填写：  
  ```python
  chao = Chaojiying_Client('你的用户名', '你的密码', '你的soft_id')  # 替换为实际信息
  ```  


### 2. 采集壁纸链接  
运行 `each_url_getting.py`，指定采集页数和 MongoDB 地址：  
```python
# 示例：采集 2 页，连接本地 MongoDB
if __name__ == '__main__':
    windows_pictures(2, 'mongodb://127.0.0.1:27017')
```  
脚本会将详情页链接（如 `https://haowallpaper.com/xxx`）和标题存储到 MongoDB 的 `哲风壁纸/解析图片` 集合。  


### 3. 下载目标图片  
运行 `基于selenium与超级鹰爬取哲风壁纸.py`，输入需要下载的图片标题关键词（支持正则匹配）：  
```bash
你想下载的图片名字：风景  # 输入关键词
```  
脚本会从 MongoDB 查找匹配的链接，逐个访问并通过验证码验证后下载图片到 `downloaded/` 目录。  


## 五、注意事项  
1. **反爬限制**：网站可能限制频繁请求，建议添加延迟（如 `time.sleep(1-3)`）或使用代理。  
2. **验证码费用**：超级鹰识别服务需付费，注意账号余额。  
3. **路径配置**：  
   - 验证码截图存储在 `picture/` 目录（需手动创建）。  
   - 图片下载路径可在 `options.add_experimental_option('prefs', {...})` 中修改。  
4. **浏览器驱动**：需根据本地 Chrome 版本下载对应 [ChromeDriver](https://chromedriver.chromium.org/)，并将可执行文件添加到环境变量或指定路径。  


## 六、许可证  
本项目仅用于学习交流，请勿用于商业用途。爬取行为需遵守目标网站的 `robots.txt` 和相关法律。