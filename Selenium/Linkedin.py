import argparse, os, time
import random
from urllib import parse
from selenium import webdriver
from bs4 import BeautifulSoup
import io


"""
	Given Job Details, create file in Jobs directory & puts the info
	Input: Job Details
	Output: None
"""
def createJobDetailFile(count, jobTitle, jobCompany, jobLocation, jobDescription):
	fileName = 'jobs/job'+ str(count) + '.txt'
	file = io.open(fileName, 'w', encoding='utf8')
	file.write(jobTitle);
	file.write(jobCompany);
	file.write(jobLocation);
	file.write(jobDescription);
	file.close()
    
"""
	Given Browser and count of total jobs needs to be retrieved, returns posted job data
	Input: Browser control & count of jobs
	Output: Files with posted job data
"""
def getJobData(browser):
	# For no duplication check
	visited = {}
	# Job Ids retrieved from links (All pages)
	jobList = []
	# To check number of jobs retrieved
	count = 0
	print("Job Data Retrieval in progress!")
	# Wait for initial page to load - 5 sec
	time.sleep(5)
	links = []
    
	page = BeautifulSoup(browser.page_source, "html.parser") #解析目标网页的HTML源码    
	# 提取网页的所有链接
	urls = browser.find_elements_by_xpath("//a")
	for url in urls:
		link = url.get_attribute("href")
		if "/jobs/view" in link:
			links.append(link)
			#print(link)  
	print("该页面共有URL：%d 个"% len(links))
	jobList = links
    
	while count < len(links):
        
		if jobList:
			# 依次取出职位的url信息
			job = jobList.pop()
			print(job)
			root = 'http://www.linkedin.com'
			roots = 'https://www.linkedin.com'
			if root not in job:
				if roots not in job:
					continue
			# 打开职位的具体信息界面
			browser.get(job)

			time.sleep(3)
			#爬取职位信息（根据class定位） 
			try:
				jobPage = BeautifulSoup(browser.page_source, "html.parser")
				jobTitle = browser.fizhiweind_element_by_class_name("jobs-top-card__job-title").get_attribute("textContent") + '\n' 
				jobCompany = browser.find_element_by_class_name("jobs-top-card__company-url").get_attribute("textContent")
				jobLocation = browser.find_element_by_class_name("jobs-top-card__bullet").get_attribute("textContent")
				browser.find_element_by_class_name("artdeco-button--icon-right").click()
				jobDescription = browser.find_element_by_class_name("jobs-description-content__text").get_attribute("textContent") + '\n'
				createJobDetailFile(count, jobTitle, jobCompany, jobLocation, jobDescription);
				count += 1    
			except:
				continue
			#返回职位总列表界面
			browser.back() 
		else:
			print("Error: No-data - Exiting")
			break
		# Prints the status/count of jobs retrieved
		print("(" + str(count) + "/"+ str(total) +" Visited/Queue)")

def Main():
	# Parsing the arguments from command line
	parser = argparse.ArgumentParser()
	# Argument - Email
	parser.add_argument("email", help="linkedin email")
	# Argument - Password
	parser.add_argument("password", help="linkedin password")
	args = parser.parse_args()

	# Opens Firefox browser
	browser = webdriver.Firefox()
	# Opens LinkedIn login page
	browser.get("https://linkedin.com/")
	#进入登录界面
	# Gets email/user name text box
	emailElement = browser.find_element_by_id("login-email")
	# Puts email argument into the email field
	emailElement.send_keys(args.email)
	# Gets password field from web pagejobPage
	passElement = browser.find_element_by_id("login-password")
	# Put passed argument of password 
	passElement.send_keys(args.password)
	# Submit the form
	passElement = browser.find_element_by_id("login-submit")
	passElement.click()
    
	os.system('clear')
	print("Success! Logged In, Data Retrieval in progress!")
    
	page = BeautifulSoup(browser.page_source, "html.parser")
# 	link0 = browser.find_element_by_id("jobs-nav-item")
# 	link0.click()
	#不能直接用xpath进行点击（仅得到Url的文本，需用browser.get(url)点击）
	#进入职位界面
	url = browser.find_element_by_xpath("/html/body/header/div/nav/ul/li[3]/a") 
	url1 = url.get_attribute('href')
	print(url1)
	browser.get(url1)

	page = BeautifulSoup(browser.page_source, "html.parser")
	#带有空格的class名字定位（若其中某一属性唯一，则仅输入一个即可，或者采用CSS定位）
	#搜索职位
	link1 = browser.find_element_by_class_name("jobs-search-box__submit-button")
	link1.click()
    
# 	for i in range(40):      
# 		getJobData(browser)
# 		print("第%d页的内容：" % i+1)
# 		time.sleep(1)
# 		browser.find_element_by_link_text("下页").click()
	getJobData(browser)        
	browser.close()

if __name__ == '__main__':
	Main()
