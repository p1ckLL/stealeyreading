import random
import nltk
from nltk.corpus import wordnet

book_file = open('theonceandfutureking.txt', 'r')
text = book_file.read()
book_file.close()
common_words = open("commonwords.txt", 'r').read().split()
common_word_found = False
cleaned_book = []
chapter_count = 97
page_count = 677
pages_per_chapter = 7
chapter = 1
page = 1

def main(chapter, page, text, chapter_count):
  generate_chapter_info(chapter, page, text, chapter_count)

def generate_chapter_info(chapter, page, text, chapter_count):
    words = generate_words()

    # Make reading log
    for i in range(1, chapter_count):
        locative_info = f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"
        word, definition = random.choice(list(words.items()))
        connotation = find_sentence(word)
        vocab = f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"
        print(locative_info)
        print(vocab)
        print(connotation + "\n")
        chapter += 1
        page += pages_per_chapter

def find_sentence(word):
  split_sentence_book = split_book(keep_spaces=True)
  for sentence in split_sentence_book:
    if word in sentence:
      return sentence
  
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

def split_book(keep_spaces):
    if keep_spaces:
      return text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace("\n", "").lower().split(".")
    else:
      return text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace(".", "").replace("\n", "").lower().split()

def generate_words():
  words = {}

  unpunctuated_book = split_book(keep_spaces=False)

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
    main(chapter, page, text, chapter_count)

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()