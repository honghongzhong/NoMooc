import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains


VIDEO_ID = "vjs_container_html5_api"
PLAY_BUTTON_ID = "playButton"
COOKIE_FILE = "zhihuishu_cookies.json"


def switch_to_video_frame(driver):
	driver.switch_to.default_content()
	try:
		driver.find_element(By.ID, VIDEO_ID)
		return True
	except Exception:
		pass

	iframes = driver.find_elements(By.TAG_NAME, "iframe")
	for iframe in iframes:
		try:
			driver.switch_to.default_content()
			driver.switch_to.frame(iframe)
			if driver.find_elements(By.ID, VIDEO_ID) or driver.find_elements(By.ID, PLAY_BUTTON_ID):
				return True
		except Exception:
			continue

	driver.switch_to.default_content()
	return False


def wait_for_video_finish(driver):
	retry_count = 0
	while True:
		has_dialog = handle_quiz_dialog(driver)
		if not switch_to_video_frame(driver):
			time.sleep(2)
			continue

		try:
			play_btn = driver.find_element(By.ID, PLAY_BUTTON_ID)
			if play_btn.is_displayed() and play_btn.is_enabled():
				play_btn.click()
				retry_count += 1
		except Exception:
			pass

		try:
			video = driver.find_element(By.ID, VIDEO_ID)
			if video.is_displayed():
				video.click()
				retry_count += 1
		except Exception:
			pass

		try:
			video = driver.find_element(By.ID, VIDEO_ID)
			duration = video.get_attribute("duration")
			current = video.get_attribute("currentTime")
			paused = video.get_attribute("paused")
			ended = video.get_attribute("ended")
			print(
				"播放状态 paused="
				+ str(paused)
				+ " current="
				+ str(current)
				+ " duration="
				+ str(duration)
				+ " dialog="
				+ str(has_dialog)
			)
			if paused in ("true", True):
				try:
					driver.execute_script("arguments[0].play();", video)
				except Exception:
					pass
			if ended in ("true", True):
				break
			if duration and current:
				try:
					if int(float(duration)) <= int(float(current)):
						break
					if float(duration) - float(current) <= 1:
						break
				except Exception:
					pass
		except Exception:
			pass

		if retry_count < 10:
			time.sleep(2)
		else:
			time.sleep(4)


def filter_catalogs(raw_items):
	filtered = []
	for item in raw_items:
		try:
			if item.find_elements(By.CSS_SELECTOR, "b.time_icofinish"):
				continue
			if item.find_elements(By.CSS_SELECTOR, "span.time"):
				filtered.append(item)
		except Exception:
			continue
	return filtered


def handle_quiz_dialog(driver):
	def try_handle_in_context():
		try:
			dialogs = driver.find_elements(By.CLASS_NAME, "el-dialog__wrapper")
			has_dialog = bool(dialogs)
		except Exception:
			has_dialog = False
		if not has_dialog:
			return False

		try:
			options = driver.find_elements(By.CLASS_NAME, "topic-item")
			if options:
				options[0].click()
				print("弹窗处理: 已点击第一个选项")
				time.sleep(1)
			else:
				print("弹窗处理: 未找到 topic-item")
		except Exception as exc:
			print("弹窗处理: 点击选项失败: " + str(exc))

		try:
			close_btns = driver.find_elements(By.CLASS_NAME, "el-dialog__headerbtn")
			if close_btns:
				close_btns[0].click()
				print("弹窗处理: 已点击关闭按钮")
				return True
			print("弹窗处理: 未找到 el-dialog__headerbtn")
		except Exception as exc:
			print("弹窗处理: 点击关闭失败: " + str(exc))

		try:
			footers = driver.find_elements(By.CLASS_NAME, "dialog-footer")
			if footers:
				buttons = footers[0].find_elements(By.CLASS_NAME, "btn")
				if buttons:
					driver.execute_script("arguments[0].click();", buttons[0])
					print("弹窗处理: 已点击 footer 按钮")
					return True
				print("弹窗处理: 未找到 dialog-footer 内 btn")
			else:
				print("弹窗处理: 未找到 dialog-footer")
		except Exception as exc:
			print("弹窗处理: 点击 footer 失败: " + str(exc))

		return True

	if try_handle_in_context():
		return True

	try:
		iframes = driver.find_elements(By.TAG_NAME, "iframe")
	except Exception:
		iframes = []

	for iframe in iframes:
		try:
			driver.switch_to.default_content()
			driver.switch_to.frame(iframe)
			if try_handle_in_context():
				driver.switch_to.default_content()
				return True
		except Exception:
			continue

	driver.switch_to.default_content()
	return False


# 读取配置
with open("config.json", "r", encoding="utf-8") as f:
	config = json.load(f)

# 启动浏览器
service = Service(executable_path="msedgedriver.exe")
options = webdriver.EdgeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Edge(service=service, options=options)
driver.get(config.get("zhihuishu_url", "https://www.zhihuishu.com"))

if os.path.exists(COOKIE_FILE):
	try:
		with open(COOKIE_FILE, "r", encoding="utf-8") as f:
			cookies = json.load(f)
		for cookie in cookies:
			driver.add_cookie(cookie)
		driver.refresh()
	except Exception:
		pass

# 登录
input("登录后打开到第一个界面并打开第一个视频，然后回车继续")

try:
	with open(COOKIE_FILE, "w", encoding="utf-8") as f:
		json.dump(driver.get_cookies(), f, ensure_ascii=True, indent=2)
except Exception:
	pass

catalogs = filter_catalogs(driver.find_elements(By.CLASS_NAME, "cataloguediv-c"))
if not catalogs:
	print("未找到 cataloguediv-c 元素，请确认已打开课程目录页面。")
	raise SystemExit(1)

total = len(catalogs)
print("共找到课程数量：" + str(total))
current_url = driver.current_url

for idx, item in enumerate(catalogs, start=1):
	try:
		title = item.text.strip()
	except Exception:
		title = ""
	print("课程" + str(idx) + ": " + title)

for idx in range(total):
	if driver.current_url != current_url:
		driver.get(current_url)
		time.sleep(2)
	catalogs = filter_catalogs(driver.find_elements(By.CLASS_NAME, "cataloguediv-c"))
	if idx >= len(catalogs):
		break

	current = catalogs[idx]
	try:
		print("准备播放：" + current.text.strip())
	except Exception:
		print("准备播放：" + str(idx + 1))
	try:
		driver.execute_script("arguments[0].scrollIntoView({block:'center'});", current)
		current.click()
	except Exception:
		try:
			ActionChains(driver).click(current).perform()
		except Exception:
			pass

	time.sleep(3)
	wait_for_video_finish(driver)
	print("已完成：" + str(idx + 1) + " / " + str(total))

print("全部课程播放完毕")
