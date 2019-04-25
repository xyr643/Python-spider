import time
import random
from multiprocessing import Pool  # 多进程
import aiohttp, asyncio # 多线程
from selenium import webdriver
import os


def writetxt(file, Cookname, Src, Main_ing, Acces, Mix_ing, Cooks, Steps, Tips, Types):
    f = open(os.path.join(file, '苋菜.txt'), 'a', encoding='utf-8')
    f.write(str(Cookname) + "|")
    f.write(str(Src) + "|")
    f.write(str(Main_ing) + "|")
    f.write(str(Acces) + "|")
    f.write(str(Mix_ing) + "|")
    f.write(str(Cooks) + "|")
    f.write(str(Steps) + "|")
    f.write(str(Tips) + "|")
    f.write(str(Types) + "|")
    f.write('\n')

 # 文本提取
def text_extr(browser, xpath):
    try:
        path = browser.find_elements_by_xpath(xpath)[0]
        text = path.text
        Text = (text.strip()).replace('\n', ' ')  # 去除空白行与换行符
        return Text
    except:
        return None

# 获取每一页URL列表
def urllist(browser):
    urls = browser.find_elements_by_xpath("//a")
    Links = []
    for url in urls:
        link = url.get_attribute("href")
        try:
            if "//home.meishichina.com/recipe-" in link:
                if link not in Links:
                    Links.append(link)
                # print(link)
        except:
            continue
    print("该页面共有URL：%d 个" % len(Links))
    return Links

# 单个食谱爬取
def recipelist(browser):
    try:
        cook = browser.find_elements_by_id("recipe_title")
        Cookname = cook[0].text
        print(Cookname)
    except:
        Cookname = ' '
    img = browser.find_element_by_xpath("//*[@id='recipe_De_imgBox']/a/img")
    Src = img.get_attribute("src")
    # 主料
    Main_ing = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/fieldset[1]")
    # 辅料
    Acces = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/fieldset[2]")
    # 配料
    try:
        Mix_ing = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/fieldset[3]")
    except:
        Mix_ing = []
    # 步骤
    Steps = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/div[5]")
    # 所属工艺
    Cooks = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/div[3]")
    # 小窍门
    key = browser.find_elements_by_xpath("/html/body/div[5]/div/div[1]/div[2]/div/div[6]")[0]
    if key.text == '小窍门':
        Tips = text_extr(browser, "/html/body/div[5]/div/div[1]/div[2]/div/div[7]")
        # 所属分类
        try:
            types = browser.find_elements_by_xpath("/html/body/div[5]/div/div[1]/div[2]/div/div[10]")[0]
            Types = types.text
            Types = str(Types).replace('所属分类：', '')
        except:
            Types = []
    else:
        Tips = []
        # 所属分类
        try:
            types = browser.find_elements_by_xpath("/html/body/div[5]/div/div[1]/div[2]/div/div[8]")[0]
            Types = types.text
            Types = str(Types).replace('所属分类：', '')
        except:
            Types = []
    return Cookname, Src, Main_ing, Acces, Mix_ing, Cooks, Steps, Tips, Types

# 单页食谱
def Getrecipe(browser, file):
    recipeList = urllist(browser)
    count = 0
    total = len(recipeList)
    while count < total:
        if recipeList:
            # 依次取出食谱的url信息
            recipe = recipeList.pop()
            print(recipe)
            root = 'https://home.meishichina.com'
            if root not in recipe:
                continue
            t = random.randint(0, 3)
            time.sleep(t)
            # 打开食谱的具体信息界面
            browser.get(recipe)
            # 得到食材列表
            Cookname, Src, Main_ing, Acces, Mix_ing, Cooks, Steps, Tips, Types = recipelist(browser)
            # 写入TXT文件中
            writetxt(file, Cookname, Src, Main_ing, Acces, Mix_ing, Cooks, Steps, Tips, Types)
        else:
            print("Error: No-data - Exiting")
            browser.quit()
            break
        count += 1
    print("(" + str(count) + "/" + str(total) + " Visited/Queue)")
    return count



def Main():
    # 打开谷歌浏览器
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions._arguments = ['disable-infobars']
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    file = "D:\Pycharm\PyCharm 2018.2.4\Recomend-system\Spider\食谱\蔬菜类\茎叶类\\"

    times = 0
    for i in range(100):  # 爬取页数
        URL = "https://www.meishichina.com/YuanLiao/XianCai/%s/" % i
        start = time.time()
        try:
            browser.get(URL)
            count = Getrecipe(browser, file)
            if count < 18:
                break
            time.sleep(3)
        except:
            print('第%s页出现异常' % i)
        end = time.time()
        times += (end - start)
        print('爬取第%s页耗时：' % i, end-start)
    print('总耗时：', times)

if __name__ == '__main__':
    Main()






