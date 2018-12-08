#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys


class ChromeOperator:
    def __init__(self, url, proxy = None):

        if proxy:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy)

            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome()


        self.driver.get(url)
        


    def click(self, elem, x, y):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        print 'click', (x,y)
        action.move_to_element_with_offset(elem, x, y)
        action.click()
        action.perform()

    def log(self, message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def waitUntilElem(self, cssSelector, desc='', slientMode = False, tabNum = None, interval = 1, refreshBlankTimeout = 15):
        if not desc:
            desc = cssSelector

        # 切换到第tabNum个tab（序号从0开始）
        if tabNum != None:
            self.driver.switch_to.window(self.driver.window_handles[tabNum])


        timepass = 0

        slientMode or self.log(u'等待载入[%s]元素' % desc)
        while True:
            try:
                elem = self.driver.find_element_by_css_selector(cssSelector)
                break
            except:
                pass
            time.sleep(interval)
            slientMode or self.log(u'.')

            timepass += interval
            if timepass > refreshBlankTimeout:      # 到了空白超时事件，如果还是空白页面的话，进行刷新
                try:
                    body = self.driver.find_element_by_css_selector("body")
                    if len(body.text[:5]) == 0: # 虽然能获取body，但内容为空，仍然算异常
                        assert False
                except:
                    self.log(u'\n超过空白超时事件%d秒，进行刷新,然后继续等待载入[%s]元素' % (refreshBlankTimeout, desc))
                    self.driver.refresh()
                    timepass = 0



            
        slientMode or self.log(u'\n')
        

        return elem

    def waitUntilCond(self, driverFun, desc='', slientMode = False, interval = 1):
        slientMode or self.log(u'等待[%s]条件成立' % desc)
        while not driverFun(self.driver):
            time.sleep(interval)
            slientMode or self.log('.')
        slientMode or self.log('\n')
            

    def closeTab(self, tab):
        self.driver.switch_to.window(tab)
        self.driver.close()

    def appendToFile(self, filename, text):
        with open(filename, 'a') as f:
            f.write(text)




if __name__ == '__main__':
    op = ChromeOperator("http://www.baidu.com")
    keyword = op.waitUntilElem("#kw", u"输入框")
    keyword.clear()
    keyword.send_keys(u"I'm crazy for loving you")
    keyword.send_keys(Keys.RETURN)

    

