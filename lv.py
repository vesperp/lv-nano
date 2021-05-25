from selenium import webdriver
import json
import requests
import argparse
from time import sleep



def SendMessage(token,message):
	url = "http://pushplus.hxtrip.com/send?token={}&title=您有新消息&content=nanobb&template=html".format(token,message)
	r = requests.get(url)
	print(r.text)

def GetInfo(token,num):
	url = "https://api-www.louisvuitton.cn/api/zhs-cn/catalog/skuavailability/{}".format(num)
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('--headless')
	# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
	browser = webdriver.Chrome()
	browser.get(url)
	# browser.get('https://api-www.louisvuitton.cn/api/zhs-cn/catalog/skuavailability/M61252')
	html = browser.page_source
	html = (html.strip('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">'))
	print(html)
	jsonstr = json.loads(html)
	if (jsonstr['skuAvailability'][0]['backOrder']) == False:
		print("no 缺货")
		SendMessage(token,"无货")
	else:
		print("yes 有货")
		SendMessage(token,"有货")
	browser.quit()

def main():
	parser = argparse.ArgumentParser(description='LV监控帮助手册')
	parser.add_argument('--token',help='pushplus发送消息所需的token')
	parser.add_argument('--code',help='需要监控的商品代码，例如NANO SPEEDY 手袋对应M61252')
	parser.add_argument('--timeout',help='监控的间隔时间，默认为60',default=60)
	args = parser.parse_args()
	code = args.code
	token = args.token
	timeout = args.timeout
	while True:
		GetInfo(token,code)
		sleep(timeout)


if __name__ == '__main__':
	main()

