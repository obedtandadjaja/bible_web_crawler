import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.select import Select

class BibleCrawler:

  def setUp(self):
    self.driver = webdriver.Chrome('/usr/local/bin/chromedriver') # path to your chromedriver
    # self.driver.get('https://www.bible.com/bible/59/REV.1.esv')
    self.driver.get('https://www.bible.com/bible/59/REV.21.ESV')
    time.sleep(1)
    self.wait = WebDriverWait(self.driver, 2)
    self.begin()

  def begin(self):
    while True:
      try:
        # wait for chapter content to load
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.book')))
        self.get_content(self.driver.find_elements_by_css_selector('div.book')[0])

        # set current chapter data
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.chapter-picker-container > .picker-label > input')))
        current_chapter = self.driver.find_elements_by_css_selector('.picker-label > input')[0].get_attribute('value')

        # get ready to click next arrow
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.next-arrow > a')))
        next_arrow_wrapper = self.driver.find_elements_by_class_name('next-arrow')[0]
        next_arrow = next_arrow_wrapper.find_elements_by_tag_name('a')[0]
        next_arrow.click()

        # wait until chapter changes
        self.wait.until(lambda driver:
          self.driver.find_elements_by_css_selector('.chapter-picker-container > .picker-label > input')[0].get_attribute('value') != current_chapter
        )
      except Exception as e:
        print(e)
        break
    self.teardown()

  def get_content(self, content):
    chapter = content.get_attribute('innerHTML')
    identifier = content.find_elements_by_class_name('chapter')[0].get_attribute('data-usfm')

    print chapter
    print identifier

    headings_and_verses = content.find_elements_by_css_selector('.verse .content, .heading')
    for text in headings_and_verses:
      print text.text

    # insert to database here #

  def teardown(self):
    time.sleep(1)
    self.driver.quit()

def main():
  parser = BibleCrawler()
  parser.setUp()

if __name__ == "__main__":
  main()
