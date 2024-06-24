# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import time
import pickle
import requests
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from pynput import mouse
from flask import request







# 大麦网主页
damai_url = "https://www.damai.cn/"
# 登录页
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
# 抢票目标页
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.56522195XbSgzE&id=800754246893&clicktitle=%E3%80%8A%E4%BD%95%E6%96%87%E7%A7%80%E3%80%8B'

# target_url ='https://m.damai.cn/app/dmfe/select-seat-biz/kylin.html?itemId=800754246893&userPromotion=false&toDxOrder=true&quickBuy=0&privilegeActId=&channel=damai_app&performId=214653200&skuId=5454039276474&projectId=220452023&rtc=1'
class Concert:
    def __init__(self):
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1   # {0:模拟登录,1:Cookie登录}自行选择登录方式
        # self.driver = webdriver.Chrome()        # 默认Chrome浏览器
        self.driver = Chrome()
        script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
        self.driver.execute_script(script)

    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
           sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)
        script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
        self.driver.execute_script(script)



    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            # 载入登录界面
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
            # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(target_url)
                script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
                self.driver.execute_script(script)
                self.get_cookie()

    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器，进入大麦网###')
        # self.driver.maximize_window()           # 最大化窗口
        # 调用登陆
        self.login()  # 先登录再说
        self.status = 2  # 登录成功标识
        print("###登录成功###")
        # 后续德云社可以讲
        # if self.isElementExist('/html/body/div[2]/div[2]/div/div/div[3]/div[2]'):
        #     self.driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div/div[3]/div[2]').click()

    def isElementExist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element(By.XPATH,element)
            return flag

        except:
            flag = False
            return flag

    def choose_ticket(self):
        if self.status == 2:  # 登录成功入口
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('确认页') == -1:  # 如果跳转到了订单结算界面就算这步成功了，否则继续执行此步
                try:
                    buybutton = self.driver.find_element(By.CLASS_NAME,'buy-link').text
                    print(buybutton)
                    if buybutton == "提交缺货登记":
                        # 改变现有状态
                        self.status = 2
                        self.driver.get(target_url)
                        script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
                        self.driver.execute_script(script)
                        print('###抢票未开始，刷新等待开始###')
                        continue
                    elif buybutton == "立即预定":
                        self.driver.find_element(By.CLASS_NAME,'buy-link').click()
                        # 改变现有状态
                        self.status = 3
                    elif buybutton == "立即购买":
                        self.driver.find_element(By.CLASS_NAME,'buy-link').click()
                        # 改变现有状态
                        self.status = 4
                    # 选座购买暂时无法完成自动化
                    elif buybutton == "不，选座购买":
                        self.driver.find_element(By.CLASS_NAME,'buy-link').click()
                        self.status = 5

                except:
                    print('###未跳转到订单结算界面###')

                title = self.driver.title
                print(title)

                # script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
                # self.driver.execute_script(script)

                if title == '选择座位':
                    # 实现选座位购买的逻辑
                    self.choice_seats()
                    time.sleep(1)

                    title = self.driver.title
                    print(title)

                    # script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
                    # self.driver.execute_script(script)

            # current_url = self.driver.current_url
            # self.driver.get(current_url)
            # script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
            # self.driver.execute_script(script)



            if title == '订单确认页':
                current_url = self.driver.current_url
                print("222222",current_url)
                res = requests.get(current_url)
                print(res.status_code)

                self.driver.get(current_url)
                script = 'Object.defineProperty(navigator,"webdriver",{get:()=>false,});'
                self.driver.execute_script(script)
                while True:
                    # 如果标题为确认订单
                    print('waiting ......')
                    if self.isElementExist('//*[@id="container"]/div/div[9]/button'):
                        self.check_order()
                        break


    # def extract_javascript_links(self,url):
    #     response = requests.get(url)
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     javascript_links = set()
    #     # 查找所有包含JavaScript链接的标签
    #     script_tags = soup.find_all('script', {'src': re.compile(r'.*\.js')})
    #     # 提取JavaScript链接
    #     for script_tag in script_tags:
    #         javascript_link = script_tag['src']
    #         javascript_links.add(javascript_link)
    #
    #     return javascript_links
    def choice_seats(self):

        while self.driver.title == '选择座位':
            #获取当前url
            # url = request.url

            # self.driver.get(url)
            # response = requests.get(url)
            # soup = BeautifulSoup(response.content, 'html.parser')
            # # 查找可选择的价格button
            # script_tags = soup.find_all('div', {'class': {"",""}})
            # for price_button in script_tags:
            #     print(price_button.getText())
            #     if price_button.getText() == "￥100":
            #         price_button.click()
            if self.isElementExist('//*[@id="app"]/div/div[4]/div[2]/button'):
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[4]/div[2]/button').click()
                break
            # position = []

            # def on_click(x, y, button, pressed):
            #     if pressed:
            #         position.append({x,y})
            #         print(f'Coordinates: ({x}, {y})')
            #         print(position)
            #
            # with mouse.Listener(on_click=on_click) as listener:
            #     listener.join()



            # while self.isElementExist('//*[@id="footer-bar"]/div[2]/div[2]/div[1]/div[1]/img'):
            #     # 座位手动选择 选中座位之后//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img 就会消失
            #     print('请快速的选择您的座位！！！')
            # # 消失之后就会出现 //*[@id="app"]/div[2]/div[2]/div[2]/div
            # while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
            #     # 找到之后进行点击确认选座
            #     self.driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status in [3, 4, 5]:
            print('###开始确认订单###')
            try:
                # 默认选第一个购票人信息
                self.driver.find_element(By.XPATH,'//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")
                print(e)
            # 最后一步提交订单
            time.sleep(0.5)  # 太快会影响加载，导致按钮点击无效
            self.driver.find_element(By.XPATH,'//div[@class = "w1200"]//div[2]//div//div[9]//button[1]').click()

    def finish(self):
        self.driver.quit()
        # os.remove('cookies.pkl')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        con = Concert()             # 具体如果填写请查看类中的初始化函数
        con.enter_concert()         # 打开浏览器
        con.choose_ticket()         # 开始抢票

    except Exception as e:
        print(e)
        con.finish()




