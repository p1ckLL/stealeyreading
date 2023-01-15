import nltk
nltk.download("wordnet")
from nltk.corpus import wordnet

book_file = open('theonceandfutureking.txt', 'r')
common_words = open("commonwords.txt", 'r').read().split()
common_word_found = False
cleaned_book = []
chapter_count = 97
page_count = 677
pages_per_chapter = 7
chapter = 1
page = 1

def generate_chapter_info():
  locative_info = "Chapter " + str(chapter) + ", Pages " + str(page) + "-" + str(page+pages_per_chapter-1)
  words = generate_words()
  
def get_definition(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    return definition

def word_exists(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    if definition:
      return True
    else:
      return False

def generate_words():
  words = {}

  unpunctuated_book = book_file.read().replace(",", "").replace("\"", "").replace("!", "").replace(".", "").replace("-", "").replace("—", "").lower().split() 

  for word in unpunctuated_book:
      for common_word in common_words:
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

print(generate_words())

book_file.close()