import time
from selenium import webdriver
from bs4 import BeautifulSoup


def writetxt(cookname, src, table_list):
    f = open('早餐.txt', 'a', encoding='utf-8')
    f.write(str(cookname)+" ")
    f.write(str(src)+" ")
    for i in range(len(table_list)):
        for j in range(len(table_list[i])):
            a = str(table_list[i][j]).replace(
'\n', ' ')
            f.write(str(a)+' ')
    f.write('\n')


def urllist(browser):
    urls = browser.find_elements_by_xpath("//a")
    Links = []
    for url in urls:
        link = url.get_attribute("href")
        if "/cookbook/" in link:
            if link not in Links:            
                Links.append(link)
            #print(link)  
    print("该页面共有URL：%d 个"% len(Links))
    return Links

def tablelist(browser):
    cook = browser.find_elements_by_class_name("text-lips")
    cookname = cook[0].text
    #print(cookname)
    img = browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/a/img")  
    src = img.get_attribute("src")
    table1 = browser.find_element_by_class_name("retamr")
    table_rows = table1.find_elements_by_tag_name("tr")
    #print(table_rows)
    table_list = []
    for tr in table_rows:
        table_cols = tr.find_elements_by_tag_name("td")
        row_list = []
        for td in table_cols:  #遍历每一个td
            row_list.append(td.text)  #取出表格的数据，并zaocna放入行列表里
        table_list.append(row_list)
        #print(table_list)
    return cookname, src, table_list
    
def Getrecipe(browser):
    page = BeautifulSoup(browser.page_source, "html.parser")
    time.sleep(2)
    recipeList = []

    recipeList = urllist(browser)

    count = 0
    total = len(recipeList)
    while count < total: 
        if recipeList:
            # 依次取出食谱的url信息
            recipe = recipeList.pop()
            print(recipe)
            root = 'http://www.douguo.com'
            roots = 'https://www.douguo.com'
            if root not in recipe:
                if roots not in recipe:
                    continue
            # 打开食谱的具体信息界面
            browser.get(recipe)
            time.sleep(2)
            #解析当前食谱的信息
            page = BeautifulSoup(browser.page_source, "html.parser")
            #得到食材列表
            cookname, src, table_list = tablelist(browser)
            #写入TXT文件中
            writetxt(cookname, src, table_list)
            #返回上一级界面
            browser.back()
        else:
            print("Error: No-data - Exiting")
            break
    print("(" + str(count) + "/"+ str(total) +" Visited/Queue)")

def Main():
    # Opens Firefox browser
    browser = webdriver.Firefox()
    # Opens xaichufang login page
    browser.get("https://www.douguo.com/")
    page = BeautifulSoup(browser.page_source, "html.parser")
    bref0 = browser.find_element_by_id("searchForm").click()
    browser.find_element_by_id("global_search_inpt").send_keys("早餐 ")
    browser.find_element_by_class_name("lib").click()
    #Getrecipe(browser)
    for i in range(3):
        Getrecipe(browser)
        browser.find_element_by_class_name("anext").click()
        time.sleep(3)

if __name__ == '__main__':
    Main()
