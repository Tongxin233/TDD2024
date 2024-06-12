from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
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
        self.assertIn('Start a new To-Do', header_text)#,"browser title was:"+self.browser.title
        
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
        # self.fail('Finish the test!')

        # 他访问这个URL，发现他的待办事项列表还在
        # 他满意地离开了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 李四新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy birds')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy birds')

        # 他注意到清单有个唯一的URL
        li4_list_url = self.browser.current_url
        self.assertRegex(li4_list_url,'/lists/.+')

        # 现在有一个新用户王五访问了网站
        # 我们使用一个新的浏览器会话
        # 确保李四的信息不会从cookie中泄露出来
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 王五访问首页
        # 页面中看不到李四的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy birds',page_text)
        self.assertNotIn('Send birds to zyz',page_text)

        # 王五输入一个新的待办事项，新建一个清单
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 王五获得了他的唯一URL
        wang5_list_url = self.browser.current_url
        self.assertRegex(wang5_list_url,'/lists/.+')
        self.assertNotEqual(wang5_list_url,li4_list_url)

        # 这个页面还是没有李四的清单
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy birds',page_text)
        self.assertIn('Buy milk',page_text)

        # 两人都很满意，然后离开了

    def test_layout_and_styling(self):
        # 李四访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # 他看到输入框完美的居中显示
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)

        # 他新建了一个清单，看到输入框仍完美的居中显示
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(inputbox.location['x']+inputbox.size['width']/2,512,delta=10)