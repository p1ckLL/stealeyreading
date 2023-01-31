import random
import requests
import re
import nltk
from nltk.corpus import wordnet
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

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
    significant_statements = generate_significant_statements()

    # Make reading log
    for i in range(1, chapter_count):
        locative_info = generate_locative_info(chapter, page, pages_per_chapter)
        word, definition = generate_word_def(words)
        connotation = find_sentence(word, split_book(keep_periods=True, return_string=False, keep_caps=False, keep_punctuation=False))
        vocab = generate_vocab(page, pages_per_chapter, word, definition)
        significant_statement = significant_statements[i%len(significant_statements)]
        main_idea = "Main Idea: " + generate_main_idea(split_on_chapters(split_book(True, True, True, False))[i]) + "\n"
        print(locative_info)
        print(vocab)
        print("Connotation: " + "\"" + connotation + "\"")
        print("Significant Statement: " + significant_statement)
        print(main_idea)
        chapter += 1
        page += pages_per_chapter

def split_on_chapters(text):
  chapters = re.split(r"(?i)Chapter \d+[^\n]+", text)
  chapters = [ch for ch in chapters if ch.strip() != ""]
  return chapters

def generate_significant_statements():
  statements = []
  for word in heroic_text:
    statement = find_sentence(word, split_book(keep_periods=True, return_string=False, keep_caps=True, keep_punctuation=False))
    if statement:
      statements.append(statement)
  return statements

def generate_main_idea(text):
  parser = PlaintextParser.from_string(text, Tokenizer("english"))
  summarizer = LexRankSummarizer()

  summary = summarizer(parser.document, 1)
  joined_summary = " ".join([str(sent) for sent in summary])

  return joined_summary

def generate_locative_info(chapter, page, pages_per_chapter):
  return f"Chapter {chapter}, Pages {page}-{page+pages_per_chapter-1}"

def generate_word_def(words):
  return random.choice(list(words.items()))

def generate_vocab(page, pages_per_chapter, word, definition):
  return f"Page {random.randint(page, page+pages_per_chapter-1)}, {word} : {definition}"

def find_sentence(word, text):
  split_sentence_book = text
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

# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()