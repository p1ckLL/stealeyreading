import random
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
        print(locative_info)
        print(vocab)
        print(connotation + "\n")
        chapter += 1
        page += pages_per_chapter

def generate_locative_info(chapter, page, pages_per_chapter):
  return f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"

def generate_word_def(words):
  return random.choice(list(words.items()))

def generate_vocab(page, pages_per_chapter, word, definition):
  return f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"

def find_sentence(word):
  split_sentence_book = split_book(keep_spaces=True)
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

def split_book(keep_spaces):
    if keep_spaces:
      return text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace("\n", "").lower().split(".")
    else:
      return text.replace(";", "").replace(",", "").replace("\"", "").replace("!", "").replace(".", "").replace("\n", "").lower().split()

def generate_words():
  words = {}

  unpunctuated_book = split_book(keep_spaces=False)

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

# if __name__ == "__main__":
#     main(chapter, page, text, chapter_count, pages_per_chapter)

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()