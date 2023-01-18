import random
import nltk
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

def main():
  generate_chapter_info()

def generate_chapter_info():
    global chapter
    global page
    words = generate_words()

    # Make reading log
    for i in range(1, chapter_count):
        locative_info = f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"
        word, definition = random.choice(list(words.items()))
        connotation = find_sentence(word)
        vocab = f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"
        print(locative_info)
        print(vocab)
        print(connotation)
        chapter += 1
        page += pages_per_chapter
  
def get_definition(word):
    definition = None
    for synset in wordnet.synsets(word):
        definition = synset.definition()
        break
    return definition

def find_sentence(word):
   split_sentence_book = book_file.read().split(".")

   for sentence in split_sentence_book:
      if word in sentence:
        return str(sentence)
      
# print(find_sentence("flashes"))

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

if __name__ == "__main__":
    main()

book_file.close()

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()