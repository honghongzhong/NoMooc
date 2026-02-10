import os
import re
import time
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# 启动浏览器
service = Service(executable_path='msedgedriver.exe')
driver = webdriver.Edge(service=service)
driver.get('https://cas.whu.edu.cn/authserver/login?service=https%3A%2F%2Fzhlj.whu.edu.cn%2FcasLogin')



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
    time.sleep(10)#等10秒钟
    # Locate the iframe element
    # 两次哦
    iframe = driver.find_element(By.ID, "iframe") 
    driver.switch_to.frame(iframe)
    try:
        iframe = driver.find_element(By.CLASS_NAME, "ans-attach-online")
    except:
        continue
    driver.switch_to.frame(iframe)
    '''
    driver.find_element(By.CLASS_NAME, "vjs-big-play-button").click()
    time.sleep(4)
    
    c_time = driver.find_element(By.CLASS_NAME, "vjs-current-time").text
    total_time = driver.find_element(By.CLASS_NAME, "vjs-duration-display").text
    total_time_by_seconds = int(total_time.split(':')[0])*60 + int(total_time.split(':')[1])
    c_time_by_seconds = int(c_time.split(':')[0])*60 + int(c_time.split(':')[1])
    time_duration = total_time_by_seconds-c_time_by_seconds
    print('差'+str(time_duration)+'秒')
    for x in range(time_duration):
        time.sleep(1)
        print('播放'+str(x)+'秒'+' /' + str(time_duration))
    '''
    
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
        if a <0.01:
            break
