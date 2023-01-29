import random
import requests
import re
import nltk
from nltk.corpus import wordnet

book_file = open('theonceandfutureking.txt', 'r')
heroic_words = open("heroicwords.txt", 'r')
common_words = open("commonwords.txt", 'r')

text = book_file.read()

heroic_text = heroic_words.read().split()
common_text = common_words.read().split()

book_file.close()
heroic_words.close()
common_words.close()

url = "https://summarize-texts.p.rapidapi.com/pipeline"

common_word_found = False
cleaned_book = []
chapter_count = 97
page_count = 677
pages_per_chapter = 7
chapter = 1
page = 1

def main(chapter, page, text, chapter_count, pages_per_chapter):
  generate_chapter_info(chapter, page, chapter_count, pages_per_chapter)

def generate_chapter_info(chapter, page, chapter_count, pages_per_chapter):
    words = generate_words()

    # Make reading log
    for i in range(1, chapter_count):
        locative_info = generate_locative_info(chapter, page, pages_per_chapter)
        word, definition = generate_word_def(words)
        connotation = find_sentence(word)
        vocab = generate_vocab(page, pages_per_chapter, word, definition)
        # significant_statement = generate_significant_statement()
        # main_idea = "Main Idea: " + generate_main_idea(split_on_chapters(split_book(True, True))[i], i) + "\n")
        print(locative_info)
        print(vocab)
        print(connotation)
        # print(main_idea)
        chapter += 1
        page += pages_per_chapter

def split_on_chapters(text):
  start = 0
  chapters = []
  
  while True:
    start = text.find("chapter", start)
    if start == -1:
      break
    end = text.find("chapter", start + 1)
    if end == -1:
      end = len(text)
    chapters.append(text[start:end])
    start = end

  return chapters

def generate_significant_statement():
  for word in heroic_text:
    statement = find_sentence(word)
    if statement:
      print(statement)

def generate_main_idea(data, chapter):
  payload = {"input": data}
  headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "a02923e06dmsh6735565cd058d37p1c7a47jsn0afe938c453b",
	"X-RapidAPI-Host": "summarize-texts.p.rapidapi.com"
  }

  response = requests.request("POST", url, json=payload, headers=headers)
  response_dict = response.json()
  print(response_dict)
  main_idea = response_dict["output"][0]["text"]
  numeral = to_roman(chapter)
  main_idea.replace("chapter " + numeral, "")

  return main_idea

def generate_locative_info(chapter, page, pages_per_chapter):
  return f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"

def generate_word_def(words):
  return random.choice(list(words.items()))

def generate_vocab(page, pages_per_chapter, word, definition):
  return f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"

def find_sentence(word):
  split_sentence_book = split_book(keep_periods=True, return_string=False, keep_caps=False, keep_punctuation=False)
  for sentence in split_sentence_book:
    if word in sentence:
      end_char = sentence.find(word) + (len(word) - 1)
      return sentence[:end_char + 20]
  
def get_definition(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    return definition
      
# print(find_sentence("laboriously"))

def word_exists(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    if definition:
      return True
    else:
      return False

def to_roman(num):
  m = ["", "M", "MM", "MMM"]
  c = ["", "C", "CC", "CCC", "CD", "D",
      "DC", "DCC", "DCCC", "CM "]
  x = ["", "X", "XX", "XXX", "XL", "L",
      "LX", "LXX", "LXXX", "XC"]
  i = ["", "I", "II", "III", "IV", "V",
      "VI", "VII", "VIII", "IX"]
  
  thousands = m[num // 1000]
  hundreds = c[(num % 1000) // 100]
  tens = x[(num % 100) // 10]
  ones = i[num % 10]
  
  ans = (thousands + hundreds +
  tens + ones)
  
  return ans

def split_book(keep_periods, return_string, keep_caps, keep_punctuation):
  text_to_clean = text
  if not keep_punctuation:
    text_to_clean = text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace("\n", "")
  if not keep_punctuation and not keep_periods:
    text_to_clean = text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace(".", "").replace("\n", "")
  if not keep_caps:
    text_to_clean = text_to_clean.lower()
  if return_string:
    return text_to_clean
  else:
    if keep_periods:
      return text_to_clean.split(".")
    else: 
      return text_to_clean.split()

def generate_words():
  words = {}

  unpunctuated_book = split_book(keep_periods=False, return_string=False, keep_caps=False, keep_punctuation=False)

  for word in unpunctuated_book:
      for common_word in common_text:
          if word != common_word:
            common_word_found = False
          if word == common_word or len(word) < 9:
            common_word_found = True
            break
      if common_word_found == False and word_exists(word):
        words[word] = get_definition(word)
        cleaned_book.append(word)
      common_word_found = False
  return words

if __name__ == "__main__":
    main(chapter, page, text, chapter_count, pages_per_chapter)
# generate_significant_statement()

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()