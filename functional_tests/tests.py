from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self,row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')

		self.assertIn(row_text, [row.text for row in rows])


	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get(self.live_server_url)

		self.assertIn('Listy',self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('liste', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
		inputbox.get_attribute('placeholder'),
		'Wpisz rzecz do zrobienia'
		)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('1: Kupic pawie piora')
		inputbox.send_keys(Keys.ENTER)

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url,'/lists/.+')
		self.check_for_row_in_list_table('1: Kupic pawie piora')

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('2: Uzyc pawich pior do zrobienia przynety')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(5)


		self.check_for_row_in_list_table('2: Uzyc pawich pior do zrobienia przynety')

		self.browser.quit()
		self.browser = webdriver.Chrome()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Kupic pawie piora', page_text)
		self.assertNotIn('zrobienia przynety', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Kupic mleko')
		inputbox.send_keys(Keys.ENTER)

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url,'/lists/.+')
		self.assertNotEqual(francis_list_url,edith_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Kupic pawie piora',page_text)
		self.assertIn('Kupic mleko',page_text)

		self.fail('Zakonczenie testu!')
