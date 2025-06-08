

# 哲风壁纸爬取工具 使用文档

## 项目简介
本工具基于 Selenium 自动化浏览器与 超级鹰 OCR 验证码识别服务，实现对 [哲风壁纸](https://haowallpaper.com/) 网站的壁纸批量爬取。主要功能包括：
- 自动翻页获取多页壁纸详情页链接
- 解析单张壁纸详情页并处理滑块验证码
- 通过超级鹰识别验证码坐标完成滑块验证（需配合超级鹰服务）

---

## 环境要求
- **Python 3.7+**（推荐 3.8 及以上）
- **Chrome 浏览器**（需与 ChromeDriver 版本匹配）
- **ChromeDriver**（需与本地 Chrome 浏览器版本一致，[下载地址](https://chromedriver.chromium.org/downloads)）
- **操作系统**：Windows/macOS/Linux（需自行适配 ChromeDriver 路径）

---

## 依赖安装
```bash
pip install selenium pillow
```
- `selenium`：用于浏览器自动化操作
- `pillow`：用于图片处理（验证码坐标验证）
- 超级鹰客户端：代码中已集成基础调用逻辑，需自行注册超级鹰账号并获取服务

---

## 使用步骤

### 1. 配置超级鹰账号
- 访问 [超级鹰官网](https://www.chaojiying.com/) 注册账号并充值（验证码识别为付费服务）
- 在代码中替换以下信息（`parse_single_url` 函数内）：
  ```python
  chao = Chaojiying_Client('你的用户名', '你的密码', '你的软密')  # 替换为实际账号信息
  ```

### 2. 配置 ChromeDriver
- 下载与本地 Chrome 浏览器版本匹配的 ChromeDriver
- 将 ChromeDriver 可执行文件路径添加到系统环境变量，或直接修改代码中 `webdriver.Chrome()` 的 `executable_path` 参数（可选）

### 3. 运行程序
```bash
python 基于selenium与超级鹰爬取哲风壁纸.py
```
- 输入需要爬取的页数（如输入 `3` 则爬取前 3 页）
- 程序将自动打开 Chrome 浏览器并执行爬取流程

---

## 功能说明
### 核心流程
1. **获取分页链接**：`get_url_list(page)` 函数通过访问 `https://haowallpaper.com/?isSel=false&page={page}` 获取单页所有壁纸详情页链接。
2. **解析单页并处理验证码**：`parse_single_url(url)` 函数执行以下操作：
   - 打开壁纸详情页并点击「下载」按钮
   - 截取验证码图片并调用超级鹰识别坐标
   - 根据坐标移动滑块完成验证（当前代码未包含图片下载逻辑，需自行补充）

### 验证码处理验证
- 程序会在验证码图片上绘制红色标记点（保存为 `parsing_dot.png`），用于人工检查超级鹰识别的坐标是否准确。

---

## 注意事项
1. **反爬限制**：网站可能存在频率限制，建议添加延迟（如 `sleep(3)`）避免 IP 封禁。
2. **验证码成本**：超级鹰识别服务需付费，建议先测试少量请求再批量爬取。
3. **图片下载补充**：当前代码仅完成验证码验证，未实现图片文件下载，需自行添加以下逻辑（示例）：
   ```python
   # 在滑块验证后，找到图片下载链接并保存
   img_download_url = driver.find_element(By.XPATH,'//img[@class="target-img"]').get_attribute('src')
   # 使用 requests 或 urllib 下载图片
   import requests
   response = requests.get(img_download_url)
   with open('壁纸.jpg', 'wb') as f:
       f.write(response.content)
   ```
4. **元素定位失效**：若网站 HTML 结构变更，需更新代码中的 XPATH 表达式（如 `//div[@class="hao-bottom-nav-end DownButtom"]/span`）。

---

## 常见问题
- **ChromeDriver 版本不匹配**：错误提示 `session not created`，需重新下载匹配版本的 ChromeDriver。
- **超级鹰识别失败**：检查账号余额或验证码类型（代码中使用 `9901` 表示「坐标选择类」，需与超级鹰后台配置一致）。
- **滑块移动不准确**：可能因验证码图片缩放导致坐标偏差，可调整 `x-width//2` 的偏移量计算逻辑。

---

## 免责声明
本工具仅用于学习交流，请勿用于商业用途或非法爬取。使用前请仔细阅读目标网站的 `robots.txt` 和服务条款，因不当使用导致的法律责任由用户自行承担。