from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pyshadow.main import Shadow
import time
import os

class WordleInterface:
  CORRECT = 2
  PRESENT = 1
  ABSENT = 0
  TBD = -1

  def __init__(self):
    #firefox_options = Options()
    #firefox_options.add_argument('--headless')
    #self._driver = webdriver.Firefox(firefox_options=firefox_options)
    #self._driver = webdriver.Firefox()
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.set_headless()
    #self._driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    options = Options()
    options.headless = True
    self._driver = webdriver.Firefox(options=options)

    #chrome_options = Options()  
    #chrome_options.add_argument("--headless")  
    ##chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'  
    #self._driver = webdriver.Chrome(chrome_options=chrome_options)

    self._driver.get("https://www.nytimes.com/games/wordle/index.html")
    self._driver.implicitly_wait(15)
    self._shadow = Shadow(self._driver)
  
    # close wordle instructions overlay
    self._shadow.find_element('div[class="close-icon"]').click()

  # todo: close properly so that object can't access driver improperly
  def close(self):
    self._driver.close()

  def clear_row(self):
    for i in range(5):
      self._shadow.find_element('button[data-key="←"]').click()

  def click_letter(self, letter):
    self._shadow.find_element('button[data-key="{}"]'.format(letter)).click()
  
  def check_word(self):
    # find the last row that has data in it
    prev_row = None
    rows = self._shadow.find_elements('game-row')
    for row in rows:
      if not row.get_attribute('letters'):
        break
      prev_row = row
    
    # read the tile row and find out which letters are correct
    results = []
    tiles = self._shadow.find_elements(prev_row, 'div[class="tile"]')
    for tile in tiles:
      if tile.get_attribute('data-state') == 'correct':
        results.append(WordleInterface.CORRECT)
      elif tile.get_attribute('data-state') == 'present':
        results.append(WordleInterface.PRESENT)
      elif tile.get_attribute('data-state') == 'absent':
        results.append(WordleInterface.ABSENT)
      else:
        results.append(WordleInterface.TBD) # assume word is not in list
    return results

  def guess_word(self, word):
    for letter in word:
      self.click_letter(letter)
    self._shadow.find_element('button[data-key="↵"]').click()
    time.sleep(5) # todo: I'm sure there's a much better way to handle this
    return self.check_word()


if __name__ == "__main__":
  wi = WordleInterface()
  wi.guess_word('alone')
  wi.guess_word('sails')