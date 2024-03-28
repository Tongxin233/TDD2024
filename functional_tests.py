from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):#把测试环境清理掉
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 李四听说有个在线待办事项应用
        # 他去看了这个应用的首页
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        table = self.browser.find_element(By.ID,'id_list_table')
        rows = table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1: Buy birds',[row.text for row in rows])

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 他输入了'Send birds to zyz'
        self.fail('Finish the test!')

        # 页面再次更新，他的清单中显示了这两个待办事项

        # 他想知道这个网站是否会记住他的清单
        # 他看到网站为他生成了一个唯一的URL

        # 他访问这个URL，发现他的待办事项列表还在
        # 他满意地离开了
if __name__ == '__main__':
    unittest.main()#程序入口
