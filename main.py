import discord
import os
from wordle_interface import WordleInterface
from repl_server import server
from wordfreq import iter_wordlist
import re
import string

client = discord.Client()
    
@client.event
async def on_ready():
  print("Mwahahah")

@client.event
async def on_message(message):
  print("message")
  return
server = server()

class WordleBot:
  def __init__(self):
    self._wordle_words = []
    self._wordle_interface = WordleInterface()
    self._word_regex = [string.ascii_lowercase,
                        string.ascii_lowercase,
                        string.ascii_lowercase,
                        string.ascii_lowercase,
                        string.ascii_lowercase]
    self._present_letters = ''

    # iterate over english words in descending frequency order
    for word in iter_wordlist('en', wordlist='best'):
      # todo: filter out plurals
      if len(word) == 5 and word.isalpha(): # make sure string is 5 letters
        self._wordle_words.append(word)
  
  def get_next_common_word(self):
    r = re.compile('[' + ']['.join(self._word_regex) + ']')
    candidates = list(filter(r.match, self._wordle_words))
    for letter in self._present_letters: # todo make this a proper regex
      r = re.compile('[a-z]*[{}]+[a-z]*'.format(letter))
      candidates = list(filter(r.match, candidates))
    print(candidates[:150])
    return candidates[0]

  def update_regex(self, word, results):
    self._present_letters = ''
    for i, letter, result in zip(range(6), word, results):
      if result == WordleInterface.CORRECT: # force a match for this letter at this position
        self._word_regex[i] = letter
      elif result == WordleInterface.PRESENT: # remove this letter from this position and add it as a requirment
        self._present_letters += letter
        self._word_regex[i] = self._word_regex[i].replace(letter, '')
      elif result == WordleInterface.ABSENT: # remove this letter from this position and add it as a requirment
        for j in range(len(self._word_regex)):
          if len(self._word_regex[j]) > 1:
            self._word_regex[j] = self._word_regex[j].replace(letter, '')
    print(self._present_letters)
    print(self._word_regex)
  
  def solve_wordle(self):
    word = None
    for x in range(6):
      word = self.get_next_common_word()
      results = self._wordle_interface.guess_word(word)

      while WordleInterface.TBD in results: # assume this is not a valid word
        self._wordle_words.remove(word)
        self._wordle_interface.clear_row()
        word = self.get_next_common_word()
        results = self._wordle_interface.guess_word(word)

      # check if we won
      if all(result == WordleInterface.CORRECT for result in results):
        break

      self.update_regex(word, results)

    share_results = self._wordle_interface.get_share_results()
    self._wordle_interface.close()

    # check if we won
    if all(result == WordleInterface.CORRECT for result in results):
      return word, share_results
    else:
      return None, share_results

if __name__ == "__main__":
  client.run(os.environ['TOKEN'])
  
  wb = WordleBot()
  word, share_results = wb.solve_wordle()
  print(word)
  print(share_results)