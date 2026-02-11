
import os
import re
import time
import math
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains


# 读取配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 启动浏览器
service = Service(executable_path='msedgedriver.exe')
driver = webdriver.Edge(service=service)
driver.get(config.get('muke_url', 'https://passport2.chaoxing.com/login?refer=http://i.mooc.chaoxing.com'))



# 登录
input('登录了之后点到第一个课程，然后回车')
all_window_handles = driver.window_handles
driver.switch_to.window(all_window_handles[-1])

# 获取视频
unfinished_videos = driver.find_elements(By.CLASS_NAME, 'posCatalog_name')
jses = []

for x in range(len(unfinished_videos)):
    # try:
    new_video = unfinished_videos[x]
    element_html = new_video.get_attribute('outerHTML')
    match = re.search(r'getTeacherAjax(.*);', element_html).group()
    jses.append(match)
    # ele = new_video
    # ActionChains(driver) \
    #     .click(ele) \
    #     .perform()
    # time.sleep(2)
    # video_url = driver.current_url
    # print('正在获取链接' + str(x) + ' /' + str(len(unfinished_videos)))
    # urls.append(video_url)
    
    # except:
        # print('失败   正在获取链接' + str(x) + ' /' + str(len(unfinished_videos)))
        # continue
        

for x in range(len(jses)):
    driver.switch_to.window(all_window_handles[-1])
    # js
    driver.execute_script(jses[x])
    print(driver.current_url)
    time.sleep(10)  # 等10秒钟
    # Locate the iframe element
    # 两次哦
    iframe = driver.find_element(By.ID, "iframe")
    driver.switch_to.frame(iframe)
    try:
        iframe = driver.find_element(By.CLASS_NAME, "ans-attach-online")
    except:
        continue
    driver.switch_to.frame(iframe)
    # ...existing code...
    js_code = '''
    const video = document.getElementById('video_html5_api');
    video.play();
    '''

    js_code2 = '''
    const video = document.getElementById('video_html5_api');
    return (video.duration - video.currentTime);'''
    driver.execute_script(js_code)
    time.sleep(3)
    js_code3 = '''
    const video = document.getElementById('video_html5_api');
    video.currentTime = video.duration;'''
    try:
        driver.execute_script(js_code3)
    except:
        pass

    while True:
        driver.execute_script(js_code)
        time.sleep(3)
        a = driver.execute_script(js_code2)
        if a < 0.01:
            break
