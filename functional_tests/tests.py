from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):#把测试环境清理掉
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,'id_list_table')
                rows = table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except(AssertionError,WebDriverException) as e:
                if time.time()-start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 李四听说有个在线待办事项应用
        # 他去看了这个应用的首页
        self.browser.get(self.live_server_url)

        # 他注意到网页的标题和头部都包含'To-Do'这个词
        self.assertIn('To-Do', self.browser.title)#,"browser title was:"+self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)#,"browser title was:"+self.browser.title
        
        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        # 他在一个文本框中输入了'Buy birds'
        inputbox.send_keys('Buy birds')

        # 他按了回车键后，页面更新了
        # 待办事项表格中显示了'1: Buy birds'
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy birds')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了'Send birds to zyz'
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Send birds to zyz')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，他的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy birds')
        self.wait_for_row_in_list_table('2: Send birds to zyz')

        # 他想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL
        self.fail('Finish the test!')

        # 他访问这个URL，发现他的待办事项列表还在
        # 他满意地离开了
