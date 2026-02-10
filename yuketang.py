import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# 启动浏览器
service = Service(executable_path='msedgedriver.exe')
driver = webdriver.Edge(service=service)
driver.get('https://changjiang.yuketang.cn/')

# 登录
input('登录之后打开课程，点到成绩单页面后回车继续')


# 获取视频
videos_se = driver.find_elements(By.CLASS_NAME, 'list-detail')[0]
all_videos = videos_se.find_elements(By.CLASS_NAME, 'study-unit')
unfinished_videos = []

for video in all_videos:
    text = video.text
    if '已完成' in text:
        pass
    else:
        unfinished_videos.append(video)

urls = []

try:
    for x in range(len(unfinished_videos)):
        new_video = unfinished_videos[x]
        ele = new_video.find_element(By.CLASS_NAME, 'name-text')
        ActionChains(driver) \
            .click(ele) \
            .perform()
        video_url = driver.current_url
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        urls.append(driver.current_url)
        driver.close()
        driver.switch_to.window(window_handles[0])
        os.system('cls')
        print('正在获取链接' + str(x) + ' /' + str(len(unfinished_videos)))
        
except:
    pass

original_window_handle = driver.current_window_handle
x = 4 # 这里设置窗口数量

window_handles = []
for k in range(x):
    driver.switch_to.new_window('window')
    driver.set_window_size(800, 300)
    driver.set_window_position(800, 100 * k)
    window_handles.append(driver.current_window_handle)

for k in range(x):
    driver.switch_to.window(window_handles[k])
    driver.get(urls[0])
    urls.pop(0)

while True:
    os.system('cls')
    for k in range(x):
        driver.switch_to.window(window_handles[k])
        finished_status = driver.find_elements(By.CLASS_NAME, 'text')[1].text
        print("窗口：" + str(k+1) + "  状态：" + finished_status + "  标题：" + driver.find_elements(By.CLASS_NAME, 'text')[0].text)
        print(finished_status)
        if finished_status == '已完成':
            if len(urls) == 0:
                continue
            driver.get(urls[0])
            urls.pop(0)
            time.sleep(3)
        if driver.find_elements(By.CLASS_NAME, 'pause_show') != []:
            try:
                ele = driver.find_element(By.CLASS_NAME, 'xt_video_bit_play_btn')
                ActionChains(driver) \
                        .click(ele) \
                        .perform()
            except: 
                pass
    print("当前还剩下的课程数量：" + str(len(urls)))
    time.sleep(10)
        
        
            

    

'''
# 打开视频
for url in urls:
    driver.switch_to.new_window('window')
    driver.set_window_size(800, 300)
    driver.set_window_position(800, 100 * x)
    driver.get(url)
    time.sleep(4)
    ele = driver.find_element(By.CLASS_NAME, 'xt_video_bit_play_btn')
    try:
        ActionChains(driver) \
                .click(ele) \
                .perform()
    except:
        pass
    time.sleep(3)
    driver.switch_to.window(original_window_handle)
    x += 1
    if x == 5:
        time.sleep(15 * 60)
        x = 0
'''